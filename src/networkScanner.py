#! /usr/bin/env python3

import ipaddress
from src.argParser import ParseClass
from src.generateReport import Report
from scapy.all import *
from datetime import datetime
import time

DEFAULT_NUM_PACKET = 5
DEFAULT_SPOOF_IP = '192.168.2.99'
MAX_NO_RESPONSE = 2               # Max number of no responses before ending traceroute
PORTSCAN_BATCH_SIZE = 256       # Batch sizes for sending packets. Adjust if packets are being lost.
TRACEROUTE_PROBES_PER_HOP = 3
DEFAULT_PORTS = [20, 21, 22, 23, 25, 53, 80, 110,
                 139, 143, 443, 445, 3306, 3389, 6969, 8000, 8080]
conf.verb = 0  # Disable Scapy verbosity by default

class TCPPortScanner:
    def __init__(self, timeout):
        '''
        name: __init__
        description: initializes the TCP Port Scanner class
        '''
        self.timeout = timeout

    def scan(self, targetIP, portList, verbose=False, moreverbose=False):
        '''
        name: scan
        description: scans for open ports on a target IP (batched sr() for speed)
        parameters: targetIP (string), portList (list), verbose (bool), moreverbose (bool)
        returns: openPorts (list)
        '''
        timeStart = datetime.now()
        openPorts = []

        if portList is None or len(portList) == 0:
            portList = DEFAULT_PORTS

        conf.verb = 1 if moreverbose else 0

        # Track open ports in the same order as portList
        openSet = set()

        for i in range(0, len(portList), PORTSCAN_BATCH_SIZE):
            chunk = portList[i:i + PORTSCAN_BATCH_SIZE]

            packets = [IP(dst=targetIP) / TCP(dport=p, flags='S')
                       for p in chunk]

            # Switched to sr instead of sr1 so multiple packets can be sent at once without waiting for each response
            answered, unanswered = sr(
                packets, timeout=self.timeout, retry=0, verbose=moreverbose)

            # Default: filtered (no response)
            status = {p: 'filtered' for p in chunk}
            rst_packets = []

            for sent, recieved in answered:
                dport = int(sent[TCP].dport)
                if recieved is None:
                    continue

                if recieved.haslayer(TCP):
                    flags = int(recieved.getlayer(TCP).flags)
                    # SYN+ACK = open
                    if (flags & 0x12) == 0x12:
                        status[dport] = 'open'
                        openSet.add(dport)
                        # Send RST
                        rst_packets.append(
                            IP(dst=targetIP) / TCP(
                                sport=int(sent[TCP].sport),
                                dport=dport,
                                flags='R',
                                seq=int(sent[TCP].seq) + 1
                            )
                        )
                    # RST+ACK = closed
                    elif (flags & 0x14) == 0x14:
                        status[dport] = 'closed'
                    else:
                        status[dport] = 'closed'

                elif recieved.haslayer(ICMP):
                    # ICMP unreachable = filtered/blocked
                    status[dport] = 'filtered'

            if rst_packets:
                send(rst_packets, verbose=moreverbose)

            if moreverbose:
                for p in chunk:
                    if status.get(p) == 'open':
                        Report().note(f"Port {p} is open\n")
                    elif status.get(p) == 'closed':
                        Report().note(f"Port {p} is closed\n")
                    else:
                        Report().note(f"Port {p} is filtered\n")

        # Return ports in the same order as the port list
        for p in portList:
            if p in openSet:
                openPorts.append(p)

        if verbose or moreverbose:
            Report().note("Scan Time: " + str(datetime.now() - timeStart) + "\n")

        return openPorts

    # def scan(self, targetIP, portList, verbose, moreverbose):
    #     '''
    #     name: scan
    #     description: This is the main worker of the program that will call of the neccessary functions to scan the ports on the target IP
    #     parameters: targetIP (string), portList (list)
    #     returns : list
    #     '''
    #     if not portList:
    #         raise RuntimeError("No valid ports were given.")
    #     openPorts = []
    #     timeStart = datetime.now()
    #     for port in portList:
    #         if self.scanPort(targetIP, port, verbose, moreverbose):
    #             openPorts.append((port))
    #     if moreverbose:
    #         Report().note(
    #             "Scan Time: " + str(datetime.now() - timeStart) + "\n")
    #     return openPorts

    def scanPort(self, targetIP, targetPort, verbose, moreverbose):
        '''
        name: scanPort
        description: This function will scan a given port on a target IP using TCP SYN packets
        parameters: targetIP (string), targetPort (integer)
        returns: bool
        '''
        if moreverbose:
            conf.verb = 1
        else:
            conf.verb = 0

        timeStart = datetime.now()

        # Crafting the TCP SYN packet
        packet = IP(dst=targetIP)/TCP(dport=targetPort, flags="S")

        # Sending the packet and waiting for a response
        response = sr1(packet, timeout=self.timeout, verbose=moreverbose)

        if response is None:
            if verbose or moreverbose:
                Report().note(f"Port {targetPort}: filtered or down\n" +
                              "Scan Time: " + str(datetime.now() - timeStart) + "\n")
            return False  # No response, port is filtered or host is down
        if response.haslayer(TCP):

            if response.getlayer(TCP).flags == 0x12:  # SYN-ACK flag
                # Send RST to close the connection
                rst_packet = IP(dst=targetIP)/TCP(dport=targetPort, flags="R")
                send(rst_packet, verbose=moreverbose)
                if verbose or moreverbose:
                    Report().note(
                        f"Port {targetPort}: open\n" + "Scan Time: " + str(datetime.now() - timeStart) + "\n")
                return True

            elif response.getlayer(TCP).flags == 0x14:  # RST-ACK flag
                if verbose or moreverbose:
                    Report().note(f"Port {targetPort}: closed\n" +
                                  "Scan Time: " + str(datetime.now() - timeStart) + "\n")
                return False
        return False


class ARPHostIdentifier:
    '''  
    name: ARPHostIdentifier
    description: This class will handle the ARP scanning of the network
    '''

    def __init__(self):
        '''
        name: __init__
        description: initializes the Host Identifier class
        '''
        pass

    def ArpScan(self, targetIP, verbose, moreverbose, whiteList):
        '''  
        name: ArpScan
        description: This will perform an ARP scan on a given IP 
        parameter: IP (String), verbose (bool), moreverbose (bool)
        return: list of tuples (IP, MAC)
        Source: https://stackoverflow.com/questions/59589190/python-arp-scanner
        author: Nikto
        '''
        if moreverbose:
            conf.verb = 1
        else:
            conf.verb = 0

        # Expand CIDR notation into list of IPs
        expandedIPs = self.expandCIDR(targetIP)

        for ip in expandedIPs.copy():
            # Make sure whitelist is not none and check if IP is in whitelist
            if whiteList and ip in whiteList:
                if moreverbose:
                    Report().note(f"Skipping whitelisted IP: {ip}\n")
                expandedIPs.remove(ip)

        arp_r = ARP(pdst=expandedIPs)
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r
        timeStart = datetime.now()
        answered, unanswered = srp(request, timeout=1, verbose=moreverbose)
        IpMacList = []
        for i in answered:
            temp = (i[1].psrc, i[1].hwsrc)
            IpMacList.append(temp)

        if moreverbose:
            Report().note(
                "Scan Time: " + str(datetime.now() - timeStart) + "\n")
        return IpMacList
    
    def expandCIDR(self, cidr):
        '''
        name: expandCIDR - not being used
        description: This function expands a CIDR notation into a list of individual IP addresses, using the ipaddress module.
        parameters: cidr (string)
        return: ipList (list of IP addresses)
        source: https://docs.python.org/3/howto/ipaddress.html
        '''
        ipList = []
        ipRange = ipaddress.ip_network(cidr, strict=False)
        for ip in ipRange.hosts():
            ipList.append(str(ip))
        return ipList


class ICMPHostScanner:
    '''  
    name: ICMPHostScanner
    description: This class will handle the ICMP scanning of the network (checking which hosts are active)
    '''

    def __init__(self, timeout):
        '''
        name: __init__
        description: initializes the ICMP Host Scanner class
        '''
        self.timeout = timeout



    def activeHostScan(self, targetIPList, IpMacList=None, verbose=False, moreverbose=False, whiteList=None):
        '''  
        name: activeHostScan
        description: This is the main worker of the class that will perform an ICMP active host scan on the given list of IPs and incorporate the results from IPMacList if given
                     This function also allows for dynamic calling in case ARP scan was not performed
        parameters: targetIPList (list), IpMacList (list of tuples), verbose (bool), moreverbose (bool), whiteList (list)
        returns : list of tuples, string
        '''
        if moreverbose:
            conf.verb = 1
        else:
            conf.verb = 0

        ipList = self.expandCIDR(targetIPList)
        for ip in ipList.copy():
            # Make sure whitelist is not none and check if IP is in whitelist
            if whiteList and ip in whiteList:
                if moreverbose:
                    Report().note(f"Skipping whitelisted IP: {ip}\n")
                ipList.remove(ip)

        existingIPs = {ip for ip,
                       mac in IpMacList} if IpMacList is not None else set()
        packets = []
        timeStart = datetime.now()
        if IpMacList is not None:
            for target in ipList.copy():
                # check to see if target is already in IpMacList
                if target in existingIPs:
                    # Print for dubbing purposes
                    if moreverbose:
                        Report().note(
                            f"Skipping host: {target}, already in IpMacList\n")
                    continue
                            
                else:
                    packets.append(self.buildICMPPacket(target))
            newIpMacList = self.activeHost(packets, verbose, moreverbose)
            if newIpMacList is not None:
                IpMacList.extend(newIpMacList)
            if moreverbose:
                Report().note(
                    "Scan Time: " + str(datetime.now() - timeStart) + "\n")
            return IpMacList
        else:
            for target in ipList:
                packets.append(self.buildICMPPacket(target))

            IpMacList = self.activeHost(packets, verbose, moreverbose)

        if moreverbose:
            Report().note(
                "Scan Time: " + str(datetime.now() - timeStart) + "\n")
            
        sourceIP = self.buildICMPPacket("8.8.8.8").getlayer(IP).src
        return IpMacList, sourceIP

    def buildICMPPacket(self, targetIP):
        '''
        name: buildICMPPacket
        description: This is an internal function that will build the ICMP Echo Request packet
        parameters: targetIP (string)
        returns: scapy packet
        '''
        packet = IP(dst=targetIP)/ICMP()
        return packet

    def activeHost(self, packets, verbose, moreverbose):
        '''
        name: activeHost
        description: This is an external function that will check to see if a host is active using ICMP Echo Requests
        parameters: packets (scapy packet), verbose (bool), moreverbose (bool)
        returns: list of tuples (IP, None)
        '''

        answered, _ = sr(
            packets, timeout=self.timeout, verbose=False,)
        IpList = []
        for packet in answered:
            if packet[1].haslayer(ICMP):
                typePacket = packet[1].getlayer(ICMP).type

                if typePacket == 0:  # Echo Reply
                    if moreverbose:
                        Report().note(
                            f"Host {packet[1].src} is active (ICMP Echo Reply received)\n")
                    currentPacket = (packet[1].src, None)
                    IpList.append(currentPacket)
                    
                elif typePacket == 3:  # Destination Unreachable
                    if moreverbose:
                        Report().note(
                            f"Host {packet[1].src} is active (ICMP Destination Unreachable received)\n")
                        
                elif typePacket == 11:  # Time Exceeded
                    if moreverbose:
                        Report().note(
                            f"Host {packet[1].src} is active (ICMP Time Exceeded received)\n")
                        
                elif typePacket == 8:  # Echo Request
                    if moreverbose:
                        Report().note(
                            f"Host {packet[1].src} is active (ICMP Echo Request received)\n")                
                    currentPacket = (packet[1].dst, None)
                    IpList.append(currentPacket)
        return IpList

    def expandCIDR(self, cidr):
        '''
        name: expandCIDR - not being used
        description: This function expands a CIDR notation into a list of individual IP addresses, using the ipaddress module.
        parameters: cidr (string)
        return: ipList (list of IP addresses)
        source: https://docs.python.org/3/howto/ipaddress.html
        '''
        ipList = []
        ipRange = ipaddress.ip_network(cidr, strict=False)
        for ip in ipRange:
            ipList.append(str(ip))
        return ipList


class ICMPHostIdentifier:

    def __init__(self, timeout):
        '''
        name: __init__
        description: initializes the Host Identifier class
        '''
        self.timeout = timeout

    def scan(self, targetIP, verbose=False):
        '''
        name: scan
        description: This is the main worker of the program that will call of the neccessary functions to identify the IP
        parameters: targetIP (string)
        returns : string
        '''
        conf.verb = 1 if verbose else 0  # Controls Verbosity of scapy
        numPackets = DEFAULT_NUM_PACKET  # The number of packets to send
        spoofIP = DEFAULT_SPOOF_IP  # This is the spoof IP for the one of the packet
        packets = self._craftICMP(spoofIP, targetIP)
        packetsReturned = self._sendPackets(packets, numPackets, verbose)
        IDlist = self._getIDs(packetsReturned)
        option = self._checkOS(IDlist)
        return option

    def _checkOS(self, IDlist):
        '''
        name: checkOS
        description: This is the function to check what type of IPID system the packets are created with
        parameters: IDlist (list)
        return: string
        '''
        if (self._checkGlobPerConn(IDlist)):  # for globally incrementing - will check for consecutive numbers from all of the packet IDs
            return 1  # Windows or FreeBSD
        # Bucket system - Will check and make sure the IDs are increasing:
        elif (self._bucketCheck(IDlist)):
            return 2  # LINUX system
        # process of elimination - PRNG - All values going in here are non sequential
        elif (self._PRNG(IDlist)):
            return 3  # MacOS or IOS
        else:
            return 4

    def _PRNG(self, ID):
        '''  
        name: PRNG
        description: checks to see if list is non sequential
        parameter: ID (list)
        return: boolean
        '''
        size = len(ID)
        downct = 0
        if (size == 2):  # cant detect PRNG with only two values
            return False
        for i in range(0, size - 1):
            if (ID[i] > ID[i+1]):
                downct += 1
        if (downct > int(size / 10)):
            return True
        else:
            return False

    def _bucketCheck(self, ID):
        '''
        name: bucketCheck
        description: This is a boolean helper function that will ensure each that each later packet has a larger ID. This does not check for noise, the previous if conditions should eliminate the need for that.
        parameter: ID (list)
        return: boolean
        '''
        ct = 0
        for i in range(0, len(ID) - 1):
            if (ID[i] >= ID[i+1]):
                ct -= 5
            if (ID[i] + 4 < ID[i+1]):
                ct += 1
        if (ct > int(len(ID) / 10)):
            return True
        else:
            return False

    def _checkGlobPerConn(self, ID):
        '''  
        name: checkGlobPerConn
        description: will check A[i]+2 is = A[(i+1)] -> accounting for the spoofed ID not being picked up - This will check if all of the numbers are consecutive
        parameter: ID (list)
        return: boolean
        '''
        for i in range(0, len(ID) - 1):
            if (ID[i] + 2 != ID[i + 1]):
                return False
        return True

    def _getIDs(self, packets):
        '''  
        name: getIDs
        description: This is a function for getting the IPIDs from the packets recieved
        parameter: packets (list)
        return: list
        '''
        IDlist = []
        for i in range(0, len(packets)):
            if (self._getPacketid(packets[i]) != None):
                IDlist.append(self._getPacketid(packets[i]))
        return IDlist

    def _craftICMP(self, spoofIP, targetIP):
        '''   
        name: craftICMP
        description: This will craft the ICMP and IP packet and put them together
        parameter: spoofIP (string), targetIP (string)
        returns list
        '''
        packets = []
        IPpacket = IP(dst=targetIP)
        packets.append(IPpacket/ICMP())
        sIPpacket = IP(dst=targetIP, src=spoofIP)
        packets.append(sIPpacket/ICMP())
        return packets

    def _sendPackets(self, packets, times, verbose=False):
        '''  
        name: sendPackets
        description: This will send the two packets a number of times and return a packet array separated by the midpoint for each packet
        parameter: packets (list), times (integer)
        return: list
        '''
        returnedPackets = []
        for i in range(0, times):
            time.sleep(1)
            returnedPackets.append(
                sr1(packets[0], verbose=False, timeout=self.timeout))
            # This wont return anything - response will be sent to spoofed IP
            send(packets[1], verbose=False)
        return returnedPackets

    def _getPacketid(self, packet):
        '''  
        name: getPacketid
        description: Will act as a way ensuring an int is in the place of packet
        parameters: packet (scapy object)
        '''
        if packet is None:
            return None
        if IP not in packet:
            return None
        if packet[IP].id is None:
            return None
        return int(packet[IP].id)


class HostStorage:
    def __init__(self):
        self.hostList = []

    def _translateOStype(self, option):
        '''  
        name: translateOStype
        description: This function is designed to handle the outputs of the network scanner, converting the results to the corresponding strings (OS versions)
        parameter: option (int)
        return: String
        '''
        match option:
            case 1:
                return "Windows or FreeBSD"
            case 2:
                return "Linux"
            case 3:
                return "MacOS or IOS"
            case 4:
                return "Unknown OS"
            case 5:
                return "Inactive Host"

    def addToList(self, IPval, MacAdd, OStype, active, traceRouteTCP, traceRouteICMP, ports):
        '''  
        name: translateOStype
        description: This is a function that will be called externally to add information into the dictionary using the IP as the key
        parameter: IPval (string), MacADD (string), OStype (int), active (bool), traceRouteTCP (list), traceRouteICMP (list), ports (list)
        '''
        self.hostList.append({"IP": IPval, "MAC": MacAdd, "HostInfo": {"OS": self._translateOStype(
            OStype), "active": active, "Time": datetime.now(), "Ports": ports, "TraceRouteTCP": traceRouteTCP, "TraceRouteICMP": traceRouteICMP}})

    def getList(self):
        '''  
        name: getList
        description: This is a function that will be called externally to extract the dictionary that was built using the addToList() function
        return: dictionary
        '''
        return self.hostList


class TraceRouteScanner:
    def __init__(self, timeout):
        '''
        name: __init__
        description: initializes the Trace Route Scanner class
        '''
        self.timeout = timeout

    def scan(self, ipList, verbose, moreverbose, maxHops=30, icmpTCPoption=1, whiteList=None):
        '''  
        name: scan
        description: This is the main worker of the program that will call of the neccessary functions to perform traceroute on the list of IPs
        parameters: ipList (list/string), maxHops (int), verbose (bool), icmpTCPoption (int 1=ICMP, 2=TCP)
        returns : list
        '''
        # Turns ipList into a list of target IP strings
        if isinstance(ipList, str):
            # Allows for Dynamic calling of function with either list or CIDR notation
            targets = self.expandCIDR(ipList) if "/" in ipList else [ipList]
            if whiteList:
                for ip in targets.copy():
                    # Make sure whitelist is not none and check if IP is in whitelist
                    if ip in whiteList:
                        if moreverbose:
                            Report().note(f"Skipping whitelisted IP: {ip}\n")
                        targets.remove(ip)
            if len(targets) == 0:
                Report().note("All target IPs are whitelisted. No traceroute performed.\n")
                return None
        else:
            targets = ipList

            # Convert to set to remove duplicates and make whiteList checking easier
            ipSet = set(ipList)

            for ip in ipSet.copy():
                # Make sure whitelist is not none and check if IP is in whitelist
                if whiteList and ip in whiteList:
                    if moreverbose:
                        Report().note(f"Skipping whitelisted IP: {ip}\n")
                    ipSet.remove(ip)
            # Convert back to list
            ipList = list(ipSet)
            if len(ipList) == 0:
                Report().note("All target IPs are whitelisted. No traceroute performed.\n")
                return None

        timeStart = datetime.now()
        traceList = []
        for ip in targets:
            if icmpTCPoption == 1:
                trace, sourceIP = self.ICMPtrace(ip, verbose, moreverbose, maxHops)
                traceList.append(trace)
            elif icmpTCPoption == 2:
                trace, sourceIP = self.TCPtrace(ip, verbose, moreverbose, maxHops)
                traceList.append(trace)
                    
            else:
                Report().note("Invalid icmpTCPoption value. Please use 1 for ICMP or 2 for TCP.\n")
                return None
        if moreverbose:
            Report().note(
                "Scan Time: " + str(datetime.now() - timeStart) + "\n")
        return traceList, sourceIP

    def ICMPtrace(self, targetIP, verbose, moreverbose, maxHops=30):
        '''  
        name: ICMPtrace
        description: This function will perform a traceroute to the target IP
        parameters: targetIP (string), maxHops (int), verbose (bool), moreverbose (bool)
        returns : list of lists [hop number, IP address, time taken (ms)]
        source: https://stackoverflow.com/questions/53112554/tcp-traceroute-in-python - may use this
        '''
        if verbose:
            conf.verb = 1
        else:
            conf.verb = 0

        traceResults = []
        counter = 0
        sourceIP = None

        for TTL in range(1, maxHops + 1):
            # Used to calculate time taken for each hop
            start = datetime.now()

            # Use counter to track consecutive no responses - allow to break early
            if counter >= MAX_NO_RESPONSE:
                break
            packet = IP(dst=targetIP, ttl=TTL) / ICMP()

            packet_base = IP(dst=targetIP, ttl=TTL) / ICMP()

            # Send 3 probes at once instead of 3 sequential sr1() calls
            probes = [IP(dst=targetIP, ttl=TTL) / ICMP(seq=i)
                      for i in range(3)]
            answered, unanswered = sr(
                probes, timeout=self.timeout, verbose=moreverbose)

            # Pick the first response
            response = answered[0][1] if answered else None

            if response is None:
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * 1000
                traceResults.append([TTL, '*', timeTaken])
                counter += 1
                continue

            if response.haslayer(ICMP):
                counter = 0
                # Used to calculate time taken for each hop
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * \
                    1000  # in milliseconds
                if response.getlayer(ICMP).type == 11:  # Time Exceeded
                    traceResults.append(
                        [TTL, response.getlayer(IP).src, timeTaken])
                    if self.checkTraceResults(traceResults) is None:
                        print(
                            "[*] Time Exceeded - Invalid traceroute results, ending traceroute.\n")
                        return None

                elif response.getlayer(ICMP).type == 0:  # Echo Reply
                    if moreverbose:
                        print("[*] Echo Reply - Target reached.\n")
                    traceResults.append(
                        [TTL, response.getlayer(IP).src, timeTaken])
                    sourceIP = response.getlayer(IP).dst
                    break

                elif response.getlayer(ICMP).type == 8:  # Echo Request
                    if moreverbose:
                        print("[*] Echo Request received - ending traceroute.\n")
                    return None
                
                elif response.getlayer(ICMP).type == 3:  # Destination Unreachable
                    if moreverbose:
                        print("[*] Destination Unreachable - Ending traceroute.\n")
                    return None

            if response.getlayer(IP).src == targetIP:
                if response.haslayer(IP):
                    sourceIP = response.getlayer(IP).src
                break
        return traceResults, sourceIP

    def TCPtrace(self, targetIP, verbose, moreverbose, maxHops=30):
        '''  
        name: TCPtrace
        description: This function will perform a TCP traceroute to the target IP
        parameters: targetIP (string), maxHops (int)
        returns : list of lists [hop number, IP address, time taken (ms)]
        '''

        traceResults = []
        counter = 0
        for TTL in range(1, maxHops + 1):
            start = datetime.now()

            if counter >= MAX_NO_RESPONSE:
                break

            # Send 3 calls at once instead of 3 sequential sr1() calls
            probes = [IP(dst=targetIP, ttl=TTL) / TCP(flags='S', dport=80)
                      for _ in range(3)]
            answered, unanswered = sr(
                probes, timeout=self.timeout, verbose=moreverbose)
            response = answered[0][1] if answered else None

            # packet = IP(dst=targetIP, ttl=ttl) / TCP(flags='S', dport=80)
            # for i in range(3):
            #     response = sr1(packet, timeout=self.timeout,
            #                    verbose=moreverbose)
            #     if response is not None:
            #         break

            if response is None:
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * \
                    1000  # in milliseconds
                traceResults.append([TTL, '*', timeTaken])
                counter += 1
                if counter >= MAX_NO_RESPONSE:
                    if verbose:
                        print(
                            "[*] Maximum number of no responses reached, ending traceroute.\n")
                    return None

                continue

            elif response.haslayer(IP):
                counter = 0
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * \
                    1000  # in milliseconds
                traceResults.append(
                    [TTL, response.getlayer(IP).src, timeTaken])
                if self.checkTraceResults(traceResults) is None:
                    return None

            else:
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * \
                    1000  # in milliseconds
                traceResults.append([TTL, '*', timeTaken])
            if response.haslayer(TCP):
                if response.getlayer(TCP).flags == 'SA':  # SYN-ACK flag
                    # Send RST to close the connection
                    rst_packet = IP(dst=targetIP)/TCP(dport=response.getlayer(
                        TCP).sport, flags="R", seq=response.getlayer(TCP).ack)
                    send(rst_packet, verbose=moreverbose)
                    break
            if response.getlayer(IP).src == targetIP:
                break
        return traceResults, response.getlayer(IP).dst

    def checkTraceResults(self, tracerouteResults):
        '''  
        name: checkTraceResults
        description: This function will check to see if the traceroute results are valid (make sure first two jumps arent all no responses)
                    This may need to be adjusted based on how we want to handle no responses - for now it works
        parameters: tracerouteResults (list)
        returns : bool
        '''
        # Prevents error if max hops is set to 1
        if tracerouteResults is None or len(tracerouteResults) < 2:
            return tracerouteResults
        if tracerouteResults[0][1] == '*' and tracerouteResults[1][1] == '*':
            return None

        # Check for consecutive responses that are the same IP (indicating a loop)
        for ttl in range(len(tracerouteResults)):
            if ttl < 1:
                continue
            if tracerouteResults[ttl][1] == tracerouteResults[ttl - 1][1]:
                return None
        return tracerouteResults

    def expandCIDR(self, cidr):
        '''
        name: expandCIDR - not being used
        description: This function expands a CIDR notation into a list of individual IP addresses, using the ipaddress module.
        parameters: cidr (string)
        return: ipList (list of IP addresses)
        source: https://docs.python.org/3/howto/ipaddress.html
        '''
        ipList = []
        ipRange = ipaddress.ip_network(cidr, strict=False)
        for ip in ipRange.hosts():
            ipList.append(str(ip))
        return ipList

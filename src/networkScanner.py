#! /usr/bin/env python3

import ipaddress
from src.argParser import ParseClass
from src.generateReport import Report
from scapy.all import *
from datetime import datetime
import sys
import time

DEFAULT_NUM_PACKET = 5
DEFAULT_SPOOF_IP = '192.168.2.99'
MAX_NO_RESPONSE = 2               # Max number of no responses before ending traceroute


class TCPPortScanner:
    def __init__(self, timeout):
        '''
        name: __init__
        description: initializes the TCP Port Scanner class
        '''
        self.timeout = timeout

    def scan(self, targetIP, portList, verbose=False):
        '''  
        name: scan
        description: This is the main worker of the program that will call of the neccessary functions to scan the ports on the target IP
        parameters: targetIP (string), portList (list)
        returns : list
        '''
        if not portList:
            raise RuntimeError("No valid ports were given.")
        openPorts = []
        for port in portList:
            if self.scanPort(targetIP, port, verbose):
                openPorts.append((port))
        return openPorts

    def scanPort(self, targetIP, targetPort, verbose=False):
        '''
        name: scanPort
        description: This function will scan a given port on a target IP using TCP SYN packets
        parameters: targetIP (string), targetPort (integer)
        returns: bool
        '''
        if verbose:
            conf.verb = 1
        else:
            conf.verb = 0

        # Crafting the TCP SYN packet
        packet = IP(dst=targetIP)/TCP(dport=targetPort, flags="S")

        # Sending the packet and waiting for a response
        response = sr1(packet, timeout=self.timeout, verbose=False)

        if response is None:
            return False  # No response, port is filtered or host is down
        if response.haslayer(TCP):
            if response.getlayer(TCP).flags == 0x12:  # SYN-ACK flag
                # Send RST to close the connection
                rst_packet = IP(dst=targetIP)/TCP(dport=targetPort, flags="R")
                send(rst_packet, verbose=False)
                return True

            elif response.getlayer(TCP).flags == 0x14:  # RST-ACK flag
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

    def ArpScan(self, targetIP, verbose=False):
        '''  
        name: ArpScan
        description: This will perform an ARP scan on a given IP 
        parameter: IP (String), verbose (bool)
        return: list of tuples (IP, MAC)
        Source: https://stackoverflow.com/questions/59589190/python-arp-scanner
        author: Nikto
        '''
        if verbose:
            conf.verb = 1
        else:
            conf.verb = 0
        arp_r = ARP(pdst=targetIP)
        br = Ether(dst='ff:ff:ff:ff:ff:ff')
        request = br/arp_r
        answered, unanswered = srp(request, timeout=1, verbose=False)

        IpMacList = []
        for i in answered:
            temp = (i[1].psrc, i[1].hwsrc)
            IpMacList.append(temp)
        return IpMacList


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

    def activeHostScan(self, targetIPList, IpMacList=None, verbose=False):
        '''  
        name: activeHostScan
        description: This is the main worker of the class that will perform an ICMP active host scan on the given list of IPs and incorporate the results from IPMacList if given
                     This function also allows for dynamic calling in case ARP scan was not performed
        parameters: targetIPList (list), IpMacList (list of tuples), verbose (bool)
        returns : list of tuples 
        '''
        ipList = self.expandCIDR(targetIPList)
        existingIPs = {ip for ip,
                       mac in IpMacList} if IpMacList is not None else set()
        packets = []
        if IpMacList is not None:
            for target in ipList:
                # check to see if target is already in IpMacList
                if target in existingIPs:
                    # Debug print statement
                    print(f'Skipping host: {target}, already in IpMacList')
                    continue
                else:
                    packets.append(self.buildICMPPacket(target))
            newIpMacList = self.activeHost(packets, verbose)
            if newIpMacList is not None:
                IpMacList.extend(newIpMacList)
            return IpMacList
        else:
            for target in ipList:
                packets.append(self.buildICMPPacket(target))

            IpMacList = self.activeHost(packets, verbose)

        return IpMacList

    def buildICMPPacket(self, targetIP):
        '''
        name: buildICMPPacket
        description: This is an internal function that will build the ICMP Echo Request packet
        parameters: targetIP (string)
        returns: scapy packet
        '''
        packet = IP(dst=targetIP)/ICMP()
        return packet

    def activeHost(self, packets, verbose=False):
        '''
        name: activeHost
        description: This is an external function that will check to see if a host is active using ICMP Echo Requests
        parameters: packets (scapy packet), verbose (bool)
        returns: list of tuples (IP, None)
        '''
        answered, unanswered = sr(
            packets, timeout=self.timeout, verbose=verbose)

        IpList = []
        for packet, _ in answered:
            if packet.haslayer(ICMP):
                currentPacket = (packet.dst, None)
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
        for ip in ipRange.hosts():
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

    def scan(self, ipList, maxHops=30, verbose=False, icmpTCPoption=1):
        '''  
        name: scan
        description: This is the main worker of the program that will call of the neccessary functions to perform traceroute on the list of IPs
        parameters: ipList (list), maxHops (int), verbose (bool), icmpTCPoption (int)
        returns : dictionary
        '''
        traceDict = {}
        if icmpTCPoption == 1:
            for ip in ipList:
                traceDict[ip] = self.ICMPtrace(ip, maxHops, verbose)
            return traceDict
        elif icmpTCPoption == 2:
            for ip in ipList:
                traceDict[ip] = self.TCPtrace(ip, maxHops, verbose)
            return traceDict
        else:
            print("Invalid icmpTCPoption value. Please use 1 for ICMP or 2 for TCP.")
            return None

    def ICMPtrace(self, targetIP, maxHops=30, verbose=False):
        '''  
        name: trace
        description: This function will perform a traceroute to the target IP
        parameters: targetIP (string), maxHops (int)
        returns : list of lists [hop number, IP address, time taken (ms)]
        source: https://stackoverflow.com/questions/53112554/tcp-traceroute-in-python - may use this
        '''
        if verbose:
            conf.verb = 1
        else:
            conf.verb = 0

        traceResults = []
        counter = 0
        
        for ttl in range(1, maxHops + 1):
            # Used to calculate time taken for each hop
            start = datetime.now()

            # Use counter to track consecutive no responses - allow to break early
            if counter >= MAX_NO_RESPONSE:
                break
            packet = IP(dst=targetIP, ttl=ttl) / ICMP()

            # Satisfy trying to ID up to 3 times for each hop
            for i in range(3):
                response = sr1(packet, timeout=self.timeout, verbose=False)
                if response is not None:
                    break

            if response is None:
                traceResults.append((ttl, '*'))
                counter += 1
                continue

            if response.haslayer(ICMP):
                counter = 0
                # Used to calculate time taken for each hop
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * 1000  # in milliseconds

                if response.getlayer(ICMP).type == 11:  # Time Exceeded
                    traceResults.append([ttl, response.src, timeTaken])
                    

                elif response.getlayer(ICMP).type == 0:  # Echo Reply
                    traceResults.append([ttl, response.src, timeTaken])
                    break

                elif response.getlayer(ICMP).type == 3:  # Destination Unreachable
                    print("Destination Unreachable from " + response.src)
                    traceResults.append([ttl, response.src, timeTaken])
                    break
            if verbose:
                print("ICMPtrace debug check")
                print(response.src)
            if response.src == targetIP:
                break

        return self.checkTraceResults(traceResults)

    def TCPtrace(self, targetIP, maxHops=30, verbose=False):
        '''  
        name: TCPtrace
        description: This function will perform a TCP traceroute to the target IP
        parameters: targetIP (string), maxHops (int)
        returns : list of lists [hop number, IP address, time taken (ms)]
        '''

        traceResults = []
        counter = 0
        for ttl in range(1, maxHops + 1):

            start = datetime.now()

            if counter >= MAX_NO_RESPONSE:
                break
            packet = IP(dst=targetIP, ttl=ttl) / TCP(flags='S', dport=80)
            for i in range(3):
                response = sr1(packet, timeout=self.timeout, verbose=False)
                if response is not None:
                    break

            if response is None:
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * 1000  # in milliseconds
                traceResults.append([ttl, '*', timeTaken])
                counter += 1
                continue

            if response.haslayer(TCP):
                counter = 0
                end = datetime.now()
                timeTaken = (end - start).total_seconds() * 1000  # in milliseconds
                traceResults.append([ttl, response.src, timeTaken])
                # SYN-ACK or RST
                if response.getlayer(TCP).flags == 'SA' or response.getlayer(TCP).flags == 'R':
                    break
            if response.src == targetIP:
                break

        return self.checkTraceResults(traceResults)

    def checkTraceResults(self, tracerouteResults):
        '''  
        name: checkTraceResults
        description: This function will check to see if the traceroute results are valid (make sure first two jumps arent all no responses)
                    This may need to be adjusted based on how we want to handle no responses - for now it works
        parameters: tracerouteResults (list)
        returns : bool
        '''
        if tracerouteResults[0][1] == '*' and tracerouteResults[1][1] == '*':
            return None
        return tracerouteResults
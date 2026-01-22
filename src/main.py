# main.py
#! /usr/bin/env python3

from datetime import datetime
from src.argParser import ParseClass
from src.generateReport import Report
from src.networkScanner import ICMPHostIdentifier, ARPHostIdentifier, HostStorage, TCPPortScanner, ICMPHostScanner, TraceRouteScanner
from src.selfScan import SelfScan


def getNetworkScannerArgs():
    '''
    name: getNetworkScannerArgs
    description: This Function utlizes the class created from src/argParser.py to parse and correct the arguments given by CLI
    parameters: none
    returns: ipList (string), portList (list), timeout (integer), verbose (bool), scanType (integer), hostID (integer)
    '''
    # Parse Arguments
    Parser = ParseClass()
    parsedArgs = Parser.parser(Parser.buildParser())
    verbose, moreverbose, ipList, portList, timeout, scanType, hostID, maxHops = parsedArgs[3], parsedArgs[
        4], parsedArgs[0], parsedArgs[1], parsedArgs[2], parsedArgs[5], parsedArgs[6], parsedArgs[7]

    return ipList, portList, timeout, verbose, moreverbose, scanType, hostID, maxHops


def main():
    '''
    name: main
    description: Main function to run the network scanner application
    parameters: none
    returns: STDOUT 
    '''
    # Parse through sys.argv using argparse library
    ipList, portList, timeout, verbose, moreverbose, scanType, hostID, maxHops = getNetworkScannerArgs()

    # Initialize Reporting
    started = datetime.now()
    report = Report()
    report.print_scan_start(ipList, portList, timeout)

    # Initialize Host Identifiers, Storage, and Port Scanner
    ICMPOSDetect = ICMPHostIdentifier(timeout)
    ARPHostDetect = ARPHostIdentifier()
    storage = HostStorage()
    portScanner = TCPPortScanner(timeout)
    ICMPhostScanner = ICMPHostScanner(timeout)
    tracerouteScanner = TraceRouteScanner(timeout)

    # handle variable initialization
    OSver = None
    openPorts = None
    tracerouteResultsTCP = None
    tracerouteResultsICMP = None
    IpMacList = None

    # Self Scan (like netstat -tuln))
    if scanType in [1, 6]:  # Self Scan
        if verbose:
            report.status("Performing Self Scan")
        selfScan = SelfScan()
        net_processes = selfScan.get_net_processes()

        content = ''
        for process_name, (protocol, local_ip, local_port, remote_ip, remote_port) in net_processes.items():
            content += f"\nProcess: {process_name}, Protocol: {protocol}, Local Address: {local_ip}:{local_port}, Remote Address: {remote_ip}:{remote_port}"

        report.boxxed("Self Scan Results", content)

        if scanType == 6:
            return

    # ARP Host Identifier
    if hostID == 1:
        # Discover Hosts using ARP Scan
        if verbose:
            report.status("Running ARP scan on: " + str(ipList))
        IpMacList = ARPHostDetect.ArpScan(ipList, verbose)

        # Create empty list if no hosts found in either of host discovery scans
        if IpMacList is None:
            IpMacList = []

        if verbose:
            report.note("Hosts discovered: " + str(len(IpMacList)) + "\n")

    # ICMP Host Identifier
    elif hostID == 2:
        # Discover Hosts using ICMP Scan
        if verbose:
            report.status("Running ICMP scan on: " + str(ipList))
        IpMacList = ICMPhostScanner.activeHostScan(ipList, None, verbose)
        if IpMacList is None:
            IpMacList = []

    for i in range(0, len(IpMacList)):

        # Extract IP and MAC from tuple
        ip = IpMacList[i][0]
        mac = IpMacList[i][1] if IpMacList[i][1] is not None else None

        # Print Status
        report.status("Scanning (" + str(i + 1) + "/" +
                      str(len(IpMacList)) + "): " + str(ip))

        # Detect OS Version - ICMP scanner (works for option all and ICMP)
        if scanType in [1, 2]:
            if verbose:
                report.status("Detecting OS on: " + str(ip))
            OSver = ICMPOSDetect.scan(ip)

        # Scan Ports -TCP scanner (works for option all and TCP)
        if scanType in [1, 3]:
            if verbose:
                report.status("Scanning TCP ports on: " + str(ip))
            openPorts = portScanner.scan(ip, portList, verbose)

        # TCP traceroute - (works for option all and TraceRouteTCP)
        if scanType in [1, 4]:
            if verbose:
                report.status("Performing TCP Traceroute on: " + str(ip))
            tracerouteResultsTCP = tracerouteScanner.TCPtrace(
                ip, maxHops=maxHops, verbose=False)

        # ICMP traceroute - (works for option all and TraceRouteICMP)
        if scanType in [1, 5]:
            if verbose:
                report.status("Performing ICMP Traceroute on: " + str(ip))
            tracerouteResultsICMP = tracerouteScanner.ICMPtrace(
                ip, maxHops=maxHops, verbose=False)

        # Store Host Information
        if OSver is not None:
            storage.addToList(ip, mac, OSver, True,
                              tracerouteResultsTCP, tracerouteResultsICMP, openPorts)
        else:
            storage.addToList(ip, mac, 4, True, tracerouteResultsTCP, tracerouteResultsICMP,
                              openPorts)  # 4 = Unknown OS

        # Print Host Report
        host = storage.getList()[-1]
        report.print_host_report(host, curr=(i + 1), total=len(IpMacList))

        # Print Open Ports
        if scanType in [1, 3]:
            if verbose:
                report.status("Printing open TCP ports for: " + str(ip))
            report.printPorts(ip, openPorts)

        # Print Traceroute Results
        if scanType in [1, 4]:  # TCP Traceroute
            if verbose:
                report.status("Printing TCP Traceroute results for: " + str(ip))
            if tracerouteResultsTCP is not None:
                report.printTraceroute(tracerouteResultsTCP)
            else:
                report.note("No TCP Traceroute results to display.")

        if scanType in [1, 5]:  # ICMP Traceroute
            if verbose:
                report.status("Printing ICMP Traceroute results for: " + str(ip))
            if tracerouteResultsICMP is not None:
                report.printTraceroute(tracerouteResultsICMP)
            else:
                report.note("No ICMP Traceroute results to display.")


    ended = datetime.now()

    # ToDo: Add list of host IPs and their OS
    # ToDo: Add total scan time, remove started and ended
    results = {
        "info": {
            "network": ipList,
            "timeout": timeout,
            "started": started,
            "ended": ended,
        },
        "hosts": storage.getList(),
    }

    report.print_scan_report(results)


if __name__ == "__main__":
    main()

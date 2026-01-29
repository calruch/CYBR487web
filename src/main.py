# main.py
#! /usr/bin/env python3

from datetime import datetime
from src.argParser import ParseClass
from src.generateReport import Report
from src.networkScanner import (
    ICMPHostIdentifier,
    ARPHostIdentifier,
    HostStorage,
    TCPPortScanner,
    ICMPHostScanner,
    TraceRouteScanner,
)
from src.traceNode import TraceTree
from src.traceVisual import Visualizer
from src.selfScan import SelfScan
from multiprocessing import Pool, Queue
import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def _scan_host_worker(task):
    ip, mac, timeout, portList, maxHops, scanType = task

    ICMPOSDetect = ICMPHostIdentifier(timeout)
    portScanner = TCPPortScanner(timeout)
    tracerouteScanner = TraceRouteScanner(timeout)

    OSver = None
    openPorts = None
    tracerouteResultsTCP = None
    tracerouteResultsICMP = None
    traceListTCP = None
    traceListICMP = None
    srcIP = None

    if scanType in [1, 2]:
        OSver = ICMPOSDetect.scan(ip)

    if scanType in [1, 3]:
        if portList is not None:
            openPorts = portScanner.scan(
                ip, portList, verbose=False, moreverbose=False)

    if scanType in [1, 4]:
        tracerouteResultsTCP = tracerouteScanner.TCPtrace(
            ip, verbose=False, moreverbose=False, maxHops=maxHops)
        if scanType == 4:
            traceListTCP = tracerouteResultsTCP[0]
            srcIP = tracerouteResultsTCP[1]

    if scanType in [1, 5]:
        tracerouteResultsICMP = tracerouteScanner.ICMPtrace(
            ip, verbose=False, moreverbose=False, maxHops=maxHops)
        traceListICMP = tracerouteResultsICMP[0]
        srcIP = tracerouteResultsICMP[1]
    return (ip, mac, OSver, openPorts, traceListTCP, traceListICMP, srcIP)

def getNetworkScannerArgs():
    '''
    name: getNetworkScannerArgs
    description: This Function utlizes the class created from src/argParser.py to 
    returns: ipList (string), portList (list), timeout (integer), verbose (bool), moreverbose (bool), scanType (integer), hostID (integer), maxHops (integer), strport (string), whiteList (string), workers (integer)
    '''
    # Parse Arguments
    Parser = ParseClass()
    parsedArgs = Parser.parser(Parser.buildParser())
    verbose, moreverbose, ipList, portList, timeout, scanType, hostID, maxHops, strport, whiteList, workers = parsedArgs[3], parsedArgs[4], parsedArgs[0], parsedArgs[1], parsedArgs[2], parsedArgs[5], parsedArgs[6], parsedArgs[7], parsedArgs[8], parsedArgs[9], parsedArgs[10]

    return ipList, portList, timeout, verbose, moreverbose, scanType, hostID, maxHops, strport, whiteList, workers


def main():
    '''
    name: main
    description: Main function to run the network scanner application
    parameters: none
    returns: STDOUT 
    '''
    # Parse through sys.argv using argparse library
    ipList, portList, timeout, verbose, moreverbose, scanType, hostID, maxHops, strport, whiteList, workers = getNetworkScannerArgs()

    # Initialize Reporting
    started = datetime.now()
    report = Report()
    report.print_scan_start(ipList, strport, timeout,
                            verbose, moreverbose, started)

    # Initialize Host Identifiers, Storage, and Port Scanner
    ICMPOSDetect = ICMPHostIdentifier(timeout)
    ARPHostDetect = ARPHostIdentifier()
    storage = HostStorage()
    portScanner = TCPPortScanner(timeout)
    ICMPhostScanner = ICMPHostScanner(timeout)
    tracerouteScanner = TraceRouteScanner(timeout)
    visualizer = Visualizer(None)
    # handle variable initialization
    if verbose or moreverbose:
        verbose = True
    OSver = None
    openPorts = None
    tracerouteResultsTCP = None
    tracerouteResultsICMP = None
    IpMacList = None
    traceResults = []
    srcIP = None

    # Self Scan (like netstat -tuln))
    if scanType in [1, 6]:  # Self Scan
        timeStart = datetime.now()
        selfScan = SelfScan()
        net_processes = selfScan.get_net_processes()

        report.printSelfScan(net_processes, verbose, moreverbose, timeStart)

        if scanType == 6:
            return

    # ARP Host Identifier
    if hostID == 1:
        timeStart = datetime.now()
        # Discover Hosts using ARP Scan
        if verbose:
            report.status("Running ARP scan on: " + str(ipList))
        IpMacList = ARPHostDetect.ArpScan(
            ipList, verbose, moreverbose, whiteList)
        # Create empty list if no hosts found in either of host discovery scans
        if IpMacList is None:
            IpMacList = []

        if verbose:
            report.note("Hosts discovered: " + str(len(IpMacList)) + "\n")
            report.note("Scan Time: " +
                        str(datetime.now() - timeStart) + "\n")

    # ICMP Host Identifier
    elif hostID == 2:
        timeStart = datetime.now()
        # Discover Hosts using ICMP Scan
        if verbose:
            report.status("Running ICMP scan on: " + str(ipList))

        IpMacList, srcIP = ICMPhostScanner.activeHostScan(
            ipList, None, verbose, moreverbose, whiteList)
        # Create empty list if no hosts found in either of host discovery scans
        if IpMacList is None:
            IpMacList = []

        if verbose:
            report.note("Hosts discovered: " + str(len(IpMacList)) + "\n")
            report.note("Scan Time: " +
                        str(datetime.now() - timeStart) + "\n")

    # No Host Discovery option
    elif hostID == 0:
        timeStart = datetime.now()
        report.note("Skipping Host Discovery as per user request.\n")

        # Traceroute TCP only
        if scanType == 4:
            timeStart = datetime.now()
            type = "TCP"
            scanList, srcIP = tracerouteScanner.scan(
                ipList, verbose=verbose, moreverbose=moreverbose, maxHops=maxHops, icmpTCPoption=2, whiteList=whiteList)
            traceResults = scanList
            if scanList is not None:
                for i in range(0, len(scanList)):
                    timeStart = datetime.now()
                    report.printTraceroute(
                        type, scanList[i], verbose, moreverbose, timeStart)

        # Traceroute ICMP only
        if scanType == 5:
            type = "ICMP"
            timeStart = datetime.now()
            scanList, srcIP = tracerouteScanner.scan(
                ipList, verbose=verbose, moreverbose=moreverbose, maxHops=maxHops, icmpTCPoption=1, whiteList=whiteList)
            traceResults = scanList
            if scanList is not None:
                for i in range(0, len(scanList)):
                    report.printTraceroute(
                        type, scanList[i], verbose, moreverbose, timeStart)

    if hostID != 0:
        
        # Parallel path (docs-style Pool.map) — preserves ordering
        if workers is not None and workers > 1 and len(IpMacList) > 1 and scanType in [1, 2, 3, 4, 5]:
            tasks = [(ip, mac, timeout, portList, maxHops, scanType)
                     for (ip, mac) in IpMacList]

            with Pool(processes=workers) as pool:
                results = pool.map(_scan_host_worker, tasks)

            for i, (ip, mac, OSver, openPorts, tracerouteResultsTCP, tracerouteResultsICMP, srcIP) in enumerate(results):
                hostStartTime = datetime.now()

                report.status("Scanning (" + str(i + 1) + "/" +
                              str(len(IpMacList)) + "): " + str(ip))

                # Print Open Ports
                if scanType in [1, 3]:
                    report.printPorts(ip, openPorts, verbose,
                                      moreverbose, hostStartTime)

                # TCP traceroute
                if scanType in [1, 4]:
                    report.printTraceroute(
                        "TCP", tracerouteResultsTCP, verbose, moreverbose, hostStartTime)

                # ICMP traceroute
                if scanType in [1, 5]:
                    report.printTraceroute(
                        "ICMP", tracerouteResultsICMP, verbose, moreverbose, hostStartTime)

                # Store Host Information
                if OSver is not None:
                    storage.addToList(ip, mac, OSver, True,
                                      tracerouteResultsTCP, tracerouteResultsICMP, openPorts)
                else:
                    storage.addToList(
                        ip, mac, 4, True, tracerouteResultsTCP, tracerouteResultsICMP, openPorts)

                # Print Host Report
                host = storage.getList()[-1]
                report.print_host_report(host, verbose=verbose, moreverbose=moreverbose,
                                         timeStart=hostStartTime, curr=(i + 1), total=len(IpMacList))
                
                # Handle traceList output
                if tracerouteResultsICMP is not None:
                    traceResults.append((ip, tracerouteResultsICMP))
                elif tracerouteResultsTCP is not None:
                    traceResults.append((ip, tracerouteResultsTCP))

        else:
            for i in range(0, len(IpMacList)):
                hostStartTime = datetime.now()

                # Reset variables for each host
                OSver = None
                openPorts = None
                tracerouteResultsTCP = None
                tracerouteResultsICMP = None


                # Extract IP and MAC from tuple
                ip = IpMacList[i][0]
                mac = IpMacList[i][1] if IpMacList[i][1] is not None else None
                # Print Status
                report.status("Scanning (" + str(i + 1) + "/" +
                              str(len(IpMacList)) + "): " + str(ip))
                # Detect OS Version - ICMP scanner (works for option all and ICMP)
                if scanType in [1, 2]:
                    timeStart = datetime.now()
                    if verbose:
                        report.status("Detecting OS on: " + str(ip))
                    OSver = ICMPOSDetect.scan(ip)
                    if verbose:
                        report.note("Scan Time: " +
                                    str(datetime.now() - timeStart) + "\n")

                # Scan Ports -TCP scanner (works for option all and TCP)
                # If there is no ports given this should not be executed.
                if scanType in [1, 3] and portList is not None:
                    timeStart = datetime.now()
                    if portList is not None:
                        if verbose:
                            report.status("Scanning TCP ports on: " + str(ip))
                        openPorts = portScanner.scan(
                            ip, portList, verbose, moreverbose)

                # Print Open Ports
                    report.printPorts(ip, openPorts, verbose,
                                      moreverbose, timeStart)

                # TCP traceroute - (works for option all and TraceRouteTCP)
                if scanType in [1, 4]:
                    timeStart = datetime.now()
                    if verbose:
                        report.status(
                            "Performing TCP Traceroute on: " + str(ip))
                    tracerouteResultsTCP = tracerouteScanner.TCPtrace(
                        ip, verbose=verbose, moreverbose=moreverbose, maxHops=maxHops)
                    if tracerouteResultsTCP is not None:
                        srcIP = tracerouteResultsTCP[1]
                    if scanType == 4:
                        traceResults.append((tracerouteResultsTCP[0]))

                    # Print Traceroute Results
                    if tracerouteResultsTCP is not None:
                        report.printTraceroute(
                            "TCP", tracerouteResultsTCP[0], verbose, moreverbose, timeStart)

                # ICMP traceroute - (works for option all and TraceRouteICMP)
                if scanType in [1, 5]:
                    timeStart = datetime.now()
                    if verbose:
                        report.status(
                            "Performing ICMP Traceroute on: " + str(ip))
                    tracerouteResultsICMP = tracerouteScanner.ICMPtrace(
                        ip, verbose=verbose, moreverbose=moreverbose, maxHops=maxHops)
                    if tracerouteResultsICMP is not None:
                        srcIP = tracerouteResultsICMP[1]
                        traceResults.append((tracerouteResultsICMP[0]))

                # Print Traceroute Results
                    if tracerouteResultsICMP is not None:
                        report.printTraceroute(
                            "ICMP", tracerouteResultsICMP[0], verbose, moreverbose, timeStart)

                # Store Host Information
                if OSver is not None:
                    storage.addToList(ip, mac, OSver, True,
                                      tracerouteResultsTCP, tracerouteResultsICMP, openPorts)
                else:
                    storage.addToList(
                        ip, mac, 4, True, tracerouteResultsTCP, tracerouteResultsICMP, openPorts)

                # Print Host Report
                host = storage.getList()[-1]
                report.print_host_report(host, verbose=verbose, moreverbose=moreverbose,
                                         timeStart=hostStartTime, curr=(i + 1), total=len(IpMacList))

 
    # Traceroute Graph 
    if scanType in [1, 4, 5]:
        if verbose:
            report.status("Generating Traceroute Graph...")
        traceTree = TraceTree(srcIP)
        traceHead = traceTree.convertListTree(traceResults)
        traceTree.printTree()

        # Print Final Report
        visualizer = Visualizer(traceHead)
        visualizer.generateGraph(outputFile='traceroute_graph.png')

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
        "hosts": storage.getList(), "total time": ended - started
    }

    report.print_scan_report(
        results, verbose, moreverbose, ended - started)


if __name__ == "__main__":
    main()

#! /usr/bin/env python3

import sys
import time
import threading


class Report:

    def _make_line(self, text, max_len):
        '''  
        name make_line
        description: helper function to make a line for boxxed function
        parameters: text (string), max_len (integer)
        returns: string
        '''
        diff = max_len - len(text)
        buffer = " " * (diff)
        return "=| " + text + buffer + " |="

    def boxxed(self, title, content):
        '''  
        name: boxxed
        description: This will print a box around the given title and content
        parameters: title (string), content (string)
        returns: none
        '''
        content_lines = content.split("\n")
        max_len = max(len(title), max(len(line) for line in content_lines))

        odd = 0
        if (max_len - len(title)) % 2 != 0:
            odd = 1
        left = "=" * ((max_len - len(title)) // 2)
        right = "=" * ((max_len - len(title)) // 2 + odd)
        first_line = left + "=| " + title + " |=" + right
        print(first_line)

        for line in content_lines:
            print(self._make_line(line, max_len))

        print("=" * len(first_line) + "\n")

    def status(self, msg):
        '''  
        name: status
        description: This will print a status message to STDOUT
        parameters: msg (string)
        returns: none
        '''
        print("[*] " + str(msg) + "\n", flush=True)

    def note(self, msg):
        '''
        name: note
        description: This will print a note message to STDOUT
        parameters: msg (string)
        returns: none
        '''
        print("[+] " + str(msg), flush=True)

    def warn(self, msg):
        '''
        name: warn
        description: This will print a warning message to STDOUT
        parameters: msg (string)
        returns: none
        '''
        print("[!] " + str(msg), flush=True)

    def print_scan_start(self, network, ports, timeout):
        '''  
        name: print_scan_start
        description: This will print the starting information for the scan
        parameters: network (string), ports (list), timeout (integer)
        returns: none
        '''
        content = ""
        content += "Network: " + str(network) + "\n"
        content += "Ports: " + str(ports) + "\n"
        content += "Timeout: " + str(timeout)
        self.boxxed("Scan Starting", content)

    def print_host_report(self, host, curr=None, total=None):
        '''
        name: print_host_report
        description: This will print the report for a single host
        parameters: host (dict), curr (integer), total (integer)
        returns: none
        ''' 
        ip = host.get("IP", "")
        mac = host.get("MAC", "")
        info = host.get("HostInfo", {})
        osname = info.get("OS", "")
        active = info.get("active", False)
        tstamp = info.get("Time", "")

        title = "Host Scan: "
        if curr is not None and total is not None:
            title += " (" + str(curr) + "/" + str(total) + ")"
        content = "IP: " + str(ip) + "\n"
        content += "MAC: " + str(mac) + "\n"
        content += "OS: " + str(osname) + "\n"
        content += "Active: " + str(active) + "\n"
        content += "Time: " + str(tstamp)

        print("\n")
        self.boxxed(title, content)

    def print_scan_report(self, results):
        '''
        name: print_scan_report
        description: This will print the final report for the entire scan
        parameters: results (dict)
        returns: none
        '''
        info = results.get("info", {})
        hosts = results.get("hosts", [])

        network = info.get("network", "")
        timeout = info.get("timeout", "")
        started = info.get("started", "")
        ended = info.get("ended", "")

        count = 0
        for h in hosts:
            if h.get("HostInfo", {}).get("active", False):
                count += 1

        lines = []
        lines.append("Network: " + str(network))
        lines.append("Timeout: " + str(timeout))
        lines.append("Hosts found: " + str(len(hosts)))
        lines.append("Active hosts: " + str(count))
        lines.append("Started: " + str(started))
        lines.append("Ended: " + str(ended))

        self.boxxed("Network Scan Summary", "\n".join(lines))

    def printTraceroute(self, tracerouteResults):
        '''
        name: print_traceroute
        description: This will print the traceroute results
        parameters: tracerouteResults (list) [0: hop number, 1: IP address, 2: time taken (ms)]
        returns: STDOUT
        '''
        content = ""
        for hop, IPadd, timeTaken in tracerouteResults:
            content += f"Hop {hop}: {IPadd} - RTT: {timeTaken} ms\n"
        self.boxxed("Traceroute Results", content.strip())

    def printPorts(self, targetIP, openPorts):
        '''
        name: print_ports
        description: This will print the open ports found on the host
        parameters: openPorts (list)
        returns: STDOUT
        '''
        content = ""
        title = "Port Scan: "
        content += f"IP: {targetIP}:\n"
        for port in openPorts:
            content += f"Port {port}\n"
        self.boxxed(title, content.strip())
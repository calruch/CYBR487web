#! /usr/bin/env python3

from datetime import datetime


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

    def boxxed(self, title, content, verbose, moreverbose, timeStart):
        '''  
        name: boxxed
        description: This will print a box around the given title and content
        parameters: title (string), content (string)
        returns: none
        '''
        content_lines = content.split("\n")
        max_len = max(len(title), max(len(line) for line in content_lines), len(
            "Scan Time: " + str(datetime.now() - timeStart))) + 4

        odd = 0
        if (max_len - len(title)) % 2 != 0:
            odd = 1
        left = "=" * ((max_len - len(title)) // 2)
        right = "=" * ((max_len - len(title)) // 2 + odd)
        first_line = left + "=| " + title + " |=" + right
        print(first_line)

        for line in content_lines:
            print(self._make_line(line, max_len))

        if verbose:
            print(self._make_line("", max_len))
            print(self._make_line("Scan Time: " +
                  str(datetime.now() - timeStart), max_len))

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

    def print_scan_start(self, network, ports, timeout, verbose, moreverbose, timeStart):
        '''  
        name: print_scan_start
        description: This will print the starting information for the scan
        parameters: network (string), ports (list), timeout (integer), verbose (bool), moreverbose (bool), timeStart (datetime)
        returns: none
        '''
        content = ""
        content += "Network: " + str(network) + "\n"
        content += "Ports: " + str(ports) + "\n"
        content += "Timeout: " + str(timeout)
        self.boxxed("Scan Starting", content, verbose, moreverbose, timeStart)

    def printSelfScan(self, net_processes, verbose, moreverbose, timeStart):
        '''
        name: print_self_scan
        description: This will print the results of the self scan
        parameters: net_processes (dict), verbose (bool), moreverbose (bool), timeStart (datetime)
        returns: none
        '''
        content = ''
        for process_name, (protocol, local_ip, local_port, remote_ip, remote_port) in net_processes.items():
            if content != '':
                content += '\n'
            content += f"Process: {process_name}, Protocol: {protocol}, Local Address: {local_ip}:{local_port}, Remote Address: {remote_ip}:{remote_port}"

        self.boxxed("Self Scan Results", content.strip(),
                    verbose, moreverbose, timeStart)

    def printTraceroute(self, type, tracerouteResults, verbose, moreverbose, time):
        '''
        name: print_traceroute
        description: This will print the traceroute results
        parameters: tracerouteResults (list) [0: hop number, 1: IP address, 2: time taken (ms)], moreverbose (bool), timeStart (datetime)
        returns: none
        '''
        content = ""
        if tracerouteResults is None or len(tracerouteResults) == 0:
            content = "No traceroute results to display."
        else:
            for hop, IPadd, timeTaken in tracerouteResults:
                content += f"Hop {hop}: {IPadd} - RTT: {timeTaken} ms\n"

        self.boxxed(type + " Traceroute Results", content.strip(),
                    verbose, moreverbose, time)

    def printPorts(self, targetIP, openPorts, verbose, moreverbose, timeStart):
        '''
        name: print_ports
        description: This will print the open ports found on the host
        parameters: openPorts (list), verbose (bool), moreverbose (bool), timeStart (datetime)
        returns: none
        '''
        content = ""
        title = "Port Scan: "

        if openPorts is None or len(openPorts) == 0:
            content += "No open TCP ports found on: " + str(targetIP)

        else:
            content += f"IP: {targetIP}:\n"
            for port in openPorts:
                content += f"Port {port}\n"

        self.boxxed(title, content.strip(), verbose, moreverbose, timeStart)

    def print_host_report(self, host, verbose, moreverbose, timeStart, curr=None, total=None):
        '''
        name: print_host_report
        description: This will print the report for a single host
        parameters: host (dict), verbose (bool), moreverbose (bool), timeStart (datetime), curr (integer), total (integer)
        returns: none
        '''
        ip = host.get("IP", "")
        mac = host.get("MAC", "")
        info = host.get("HostInfo", {})
        osname = info.get("OS", "")
        active = info.get("active", False)
        tstamp = info.get("Time", "")

        title = "Host Scan Results: "
        if curr is not None and total is not None:
            title += " (" + str(curr) + "/" + str(total) + ")"
        content = "IP: " + str(ip) + "\n"
        content += "MAC: " + str(mac) + "\n"
        content += "OS: " + str(osname) + "\n"
        content += "Active: " + str(active) + "\n"
        content += "Time: " + str(tstamp)

        self.boxxed(title, content, verbose, moreverbose, timeStart)

    def print_scan_report(self, results, verbose, moreverbose, timeStart):
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

        self.boxxed("Network Scan Summary", "\n".join(
            lines), verbose, moreverbose, timeStart)

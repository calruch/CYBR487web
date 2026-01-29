#! /usr/bin/env python3

import argparse
import ipaddress
import re

DEFAULT_TIMEOUT_VALUE = 2
DEFAULT_MIN_PORT = 1
DEFAULT_MAX_PORT = 65535


class ParseClass:
    '''
    name: ParseClass
    description: This class contains methods to parse command line arguments for a network scanner tool.
    parameters: None
    return: parsedArgs (dictionary)
    usage: 
        Parser = ParseClass() # Will return arguments
        args = Parser.buildParser()
        parsedArgs = parseClass.parser(args) # Will return Dictionary
    '''

    def __init__(self):
        self.EXCLUSIVE_HOST_ADD = True  # True = Broadcast and network IP excluded

    def toggleHostSetting(self, option):
        if option is True or option is False:  # ensure it is a bool that is passed in
            self.EXCLUSIVE_HOST_ADD = option

    def buildParser(self):
        '''
        name: buildParser
        description: This function will utilize sys.argv input to parse out the arguments
        parameters: none
        return: none
        '''
        parser = argparse.ArgumentParser(
            description='This program is a network scanner tool', add_help=False)
        parser.add_argument(
            '--network', help='Target network in CIDR notation (--network=192.168.1.0/24)')
        parser.add_argument('--timeout',
                            help='Time in seconds until timeout')
        parser.add_argument(
            '--ports', help='The list of ports you would like to scan (--ports=1-1023 or --ports=5 or --ports=22 80 53)')
        parser.add_argument('-v', '--verbose',
                            help='Show verbose output', action="store_true", default=False)
        parser.add_argument('-vv', '--moreverbose',
                            help='Show more verbose output', action="store_true", default=False)
        parser.add_argument(
            '-h', '--help', help='Show usage of the program', action="store_true")
        parser.add_argument(
            '--hostid', help='Choose the host identifier type[ARP, ICMP, NONE]', default="ARP")
        parser.add_argument(
            '-m', '--maxhops', help='Maximum number of hops for traceroute', default=30, type=int)
        parser.add_argument('--scanType', choices=['all', 'OS', 'PS', 'TRTCP', 'TRICMP', 'SS'],
                            help='Choose the scan type[all, OS(ICMP OS detection), PS (TCP port scanner), TRTCP (Traceroute TCP), TRICMP (Traceroute ICMP), SS (Self Scan)]', default="all")
        parser.add_argument(
            '--workers', help='Number of worker processes for parallel host scanning (default: 1)', default=1, type=int)
        parser.add_argument('--file', help='Input file', default=None)
        args = vars(parser.parse_args())
        return args

    def whitelistCreator(self, file):
        ''' 
        name: whitelistCreator
        description: This function creates a whitelist set from the input file if provided.
        parameters: file (string)
        return: whitelist (set) or None
        '''

        whitelist = set()

        if file is None:
            whitelist = None
        else:
            try:
                with open(file, 'r') as f:
                    file = f.read().split()
                    for line in file:
                        curLine = line.strip()
                        if curLine != '' and self.validateIPCIDR(curLine):
                            whitelist.update(self.expandCIDR(curLine))
            except Exception as e:
                raise RuntimeError("Error reading input file: " + str(e))
        return whitelist

    def parser(self, args):
        '''
        name: parser
        description: This function sets up the argument parser and parses the command line arguments.
        parameters: None
        return: (tuple)
        '''

        # Whitelist file parsing - will return a set or None
        whitelist = self.whitelistCreator(args['file'])

        # Network parsing - may return None if invalid IP or CIDR given - ensure self scan is selected if no host is given
        ipList = self.parseNetwork(args['network'])
        if ipList is None and args['scanType'] != 'SS':
            raise RuntimeError("No valid IPs were retrieved")

        # Port parsing - call the parsePorts function to get a list of all of the enumerated IP's
        if args['ports'] is not None:
            portList = self.parsePorts(args['ports'])
            strport = args['ports']
        else:
            portList = None
            strport = None

        # Timeout parsing
        if args['timeout'] is not None:
            # Will check if timeout is within the bounds and sets timeout to default value if input is invalid or out of bounds.
            if self.validateTimeout(args['timeout']):
                timeoutVal = int(args['timeout'])
            else:
                timeoutVal = DEFAULT_TIMEOUT_VALUE

        else:
            timeoutVal = DEFAULT_TIMEOUT_VALUE

        # Verbose parsing
        VerboseOption = args['verbose']
        MoreVerboseOption = args.get('moreverbose', False)

        # Host Identifier parsing:
        if args['hostid'] is None:
            hostID = 1  # Default to ARP
        if args['hostid'] == 'ARP':
            hostID = 1
        elif args['hostid'] == 'ICMP':
            hostID = 2
        elif args['hostid'] == 'NONE':
            hostID = 0
        else:
            raise RuntimeError("Invalid host identifier was given")

        if args['maxhops'] < 1 or args['maxhops'] > 60:
            raise RuntimeError("Invalid max hops value was given")
        maxHops = args['maxhops']

        workers = int(args.get('workers', 1))
        if workers < 1 or workers > 64:
            raise RuntimeError('Invalid workers value was given')

        if args['scanType'] is None:
            raise RuntimeError("No scan type was given")

        # Scan type parsing:
        # option 1 - all, option 2 - ARP, option 3 - ICMP, option 4 - TCP, option 5 - TraceRouteTCP, option 6 - TraceRouteICMP, option 7 - self scan
        # Returns tuple of: (0: ipList, 1: portList, 2: timeoutVal, 3: VerboseOption, 4: MoreVerboseOption, 5: scanType, 6: hostID, 7: maxHops, 8: strport, 9: whitelist, 10: workers)
        if (args['scanType'] == 'all'):
            return (ipList, portList, timeoutVal, VerboseOption, MoreVerboseOption, 1, hostID, maxHops, strport, whitelist, workers)
        elif (args['scanType'] == 'OS'):
            return (ipList, portList, timeoutVal, VerboseOption,  MoreVerboseOption, 2, hostID, maxHops, strport, whitelist, workers)
        elif (args['scanType'] == 'PS'):
            return (ipList, portList, timeoutVal, VerboseOption, MoreVerboseOption, 3, hostID, maxHops, strport, whitelist, workers)
        elif (args['scanType'] == 'TRTCP'):
            return (ipList, portList, timeoutVal, VerboseOption, MoreVerboseOption, 4, hostID, maxHops, strport, whitelist, workers)
        elif (args['scanType'] == 'TRICMP'):
            return (ipList, portList, timeoutVal, VerboseOption, MoreVerboseOption, 5, hostID, maxHops, strport, whitelist, workers)
        elif (args['scanType'] == 'SS'):
            return (ipList, portList, timeoutVal, VerboseOption, MoreVerboseOption, 6, hostID, maxHops, strport, whitelist, workers)
        else:
            raise RuntimeError("Invalid scan type was given")

    def validateTimeout(self, timeout):
        '''
        name: ValidateTimeout 
        description: This function is designed to validate the timeout given from the userinput that was given as a command line argument
        parameters: timeout (string)
        return: boolean
        '''
        check = False
        if self.validateInteger(timeout) == False:
            return False
        elif int(timeout) < 1 or int(timeout) > 300:
            return False
        else:
            return True

    def validateInteger(self, timeout):
        '''
        name: validateInteger
        description: This function will validate that all of the chars within the timeout string are integers. This is to avoid any errors when converting the string to an integer.
        parameters: timeout (string)
        return: boolean
        '''
        isValid = bool(re.fullmatch(r'^[0-9]+$', timeout))
        return isValid

    def validateIPCIDR(self, network):
        '''
        name: validateIPCIDR
        description: This function validates if the given string is a valid IP address with optional CIDR notation.
        parameters: network (string)
        return: boolean
        disclaimer: The following regex expression was sourced from chatGPT see /gpt/AIlog.txt for more details.
        '''
        isValid = bool(re.fullmatch(r'(^(?:(?:10\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))|(?:172\.(?:1[6-9]|2\d|3[01])\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))|(?:192\.168\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))|(?:(?!10\.)(?!127\.)(?!169\.254\.)(?!192\.168\.)(?!172\.(?:1[6-9]|2\d|3[01])\.)(?:[1-9]\d?|1\d\d|2[0-1]\d|22[0-3])\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d))))(?:/(?:3[0-2]|[12]?\d))?$', network))
        return isValid

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

    def parseNetwork(self, network):
        '''
        name: parseNetwork
        description: This function parses the network string and returns the IP and CIDR if valid.
        parameters: network (string)
        return: ipList (list of IP addresses) 
        '''
        if network is None:
            return None

        if self.validateIPCIDR(network):
            # Check if CIDR notation is present
            if '/' in network:
                return network
            else:
                return network + '/32'
        else:
            return None

    def checkPort(self, port):
        '''
        name: checkPort
        description: This function checks if a given port number is valid (between 1 and 65535).
        parameters: port (int)
        return: boolean
        '''
        if port < DEFAULT_MIN_PORT or port > DEFAULT_MAX_PORT:
            return False
        else:
            return True

    def parsePorts(self, ports):
        '''
        name: parsePorts
        description: This function takes in a string of ports and returns a list of integers representing the ports to be scanned.
        parameters: ports (string) 
        return: portList (list of integers) or None if invalid
        '''
        portList = []

        if ports.startswith('-'):
            raise RuntimeError("Negative port was given")
        # option 1: user created a range of ports (1-1024)
        if '-' in ports:
            strStart, strEnd = ports.split('-')
            if strStart == '':  # Will execute if negative number is entered into ports
                raise RuntimeError("Negative port was given")
            # Convert string inputs to integers
            start = int(strStart.strip())
            end = int(strEnd.strip())

            # Run checks and adjustments on start and end ports
            if start > DEFAULT_MAX_PORT and end > DEFAULT_MAX_PORT:
                return None  # If both ports are above max, return none
            if start < DEFAULT_MIN_PORT and end < DEFAULT_MIN_PORT:
                return None  # If both ports are below min, return none
            if start > end:
                start, end = end, start  # Swap if out of order
            if self.checkPort(int(start)) == False:
                start = DEFAULT_MIN_PORT  # Set to min if port is invalid
            if self.checkPort(int(end)) == False:
                end = DEFAULT_MAX_PORT  # set to max if port is invalid

            # Create list of ports in range between start and end
            portList = list(range(start, end + 1, 1))

            return portList

        # option 2: user created a space separated list of ports (22 80 443)
        elif ',' in ports:
            strPortList = ports.split(',')

            # ensure all ports in list are valid
            for port in strPortList[:]:
                if self.checkPort(int(port)) == False:
                    strPortList.remove(port)

            # remap string list to integer list
            portList = list(map(int, strPortList))

            # If empty list return None
            if portList:
                return portList
            else:
                return None

        # option 3: user created a single port (22)
        else:
            if self.checkPort(int(ports)) == False:
                return None
            else:
                portList.append(int(ports))
                return portList

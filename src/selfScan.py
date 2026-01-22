import os
import socket


class SelfScan:
    def get_sockets(self):
        '''
        name: get_sockets
        description: Scans the /proc filesystem to find processes with open sockets
        return: sockets (dict)
        '''
        sockets = {}
        for process_id in os.listdir("/proc"):
            if not process_id.isdigit():
                continue
            try:
                # Process name
                comm = open(f"/proc/{process_id}/comm").read().strip()
                fd_dir = f"/proc/{process_id}/fd"
                for fd in os.listdir(fd_dir):
                    try:
                        thing = os.readlink(f"{fd_dir}/{fd}")
                        if thing.startswith("socket:"):
                            sockets.setdefault(comm, set()).add(
                                thing.strip("socket:[]"))
                    except OSError:
                        pass
            except OSError:
                pass

        # Prints all processes with sockets: For testing
        # for name, s in sockets.items():
        #    print(f"{name}{s}\n ")

        return sockets

    def get_net(self):
        '''
        name: get_net
        description: Reads /proc/net/tcp and /proc/net/udp to find network connections
        return: net (dict)
        '''
        net = {}
        with open("/proc/net/tcp", "r") as f:
            lines = f.readlines()[1:]
            protocol = 'tcp'
            for line in lines:
                parts = line.split()
                local_address = parts[1]
                remote_address = parts[2]
                state = parts[3]
                inode = parts[9]
                local_port = int(local_address.split(":")[1], 16)
                remote_port = int(remote_address.split(":")[1], 16)
                local_ip = socket.inet_ntoa(bytes.fromhex(
                    local_address.split(":")[0])[::-1])
                remote_ip = socket.inet_ntoa(bytes.fromhex(
                    remote_address.split(":")[0])[::-1])
                net[inode] = (protocol, local_ip, local_port,
                              remote_ip, remote_port, state)
        with open("/proc/net/udp", "r") as f:
            lines = f.readlines()[1:]
            protocol = 'udp'
            for line in lines:
                parts = line.split()
                local_address = parts[1]
                remote_address = parts[2]
                state = parts[3]
                inode = parts[9]
                local_port = int(local_address.split(":")[1], 16)
                remote_port = int(remote_address.split(":")[1], 16)
                local_ip = socket.inet_ntoa(bytes.fromhex(
                    local_address.split(":")[0])[::-1])
                remote_ip = socket.inet_ntoa(bytes.fromhex(
                    remote_address.split(":")[0])[::-1])
                net[inode] = (protocol, local_ip, local_port,
                              remote_ip, remote_port, state)

        # Prints all network connections: For testing
        # for inode, (protocol, local_ip, local_port, remote_ip, remote_port, state) in net.items():
        #    print(f"Inode: {inode}, Protocol: {protocol}, Local Address: {local_ip}:{local_port}, Remote Address: {remote_ip}:{remote_port}, State: {state}\n ")
        return net

    def get_net_processes(self):
        '''
        name: get_net_processes
        description: Maps network connections to processes using inodes
        return: net_processes (dict)
        '''
        sockets = self.get_sockets()
        net = self.get_net()
        net_processes = {}

        for name, s in sockets.items():
            for inode in s:
                if inode in net:
                    # 0A = TCP Listen, 07 = UDP Established
                    if net[inode][5] in ('0A', '07'):
                        net_processes[name] = (
                            net[inode][0], net[inode][1], net[inode][2], net[inode][3], net[inode][4])

        # Prints mapping of processes to network connections: For testing
        # for name, (protocol, local_ip, local_port, remote_ip, remote_port) in net_processes.items():
        #     print(
        #         f"Process: {name}, Protocol: {protocol}, Local Address: {local_ip}:{local_port}, Remote Address: {remote_ip}:{remote_port}\n ")

        return net_processes


# SelfScan().get_sockets()
# SelfScan().get_net()
# SelfScan().get_net_processes()

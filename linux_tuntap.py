'''

Author: Arie Gluzman
Creation Date: 13.1.2021

for further explanation on tun device - https://www.freebsd.org/cgi/man.cgi?query=tun&sektion=4

'''

import os
import fcntl
import struct

# TUN/TAP device flags #
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000
'''
Flags:
 TUNSETIFF  - Multi-Queue can be called using same file descriptor
 IFF_TUN    - layer 3, TUN device (no Ethernet headers)
 IFF_TAP    - layer 2, TAP device
 IFF_NO_PI  - Do not provide packet information
'''


# end #

class device:

    def __init__(self, mode, name=b'tun%d'):
        '''
        :param mode: hex array containing the composition of flags
        :param name: byte array containing format string of the name
        '''
        self.mode = mode
        if type(name) != bytes:
            raise ValueError("'name' must be a byte array type, not %s." % type(name))

        # Create the tun interface
        self._file_descriptor = os.open("/dev/net/tun", os.O_RDWR)
        ifr = struct.pack('16sH', name, mode)  # Create C struct of flags (device mode) and device name
        ifname_bytes = fcntl.ioctl(self._file_descriptor, TUNSETIFF,
                                   ifr)  # send struct to Kernel to manipulate device-at file-descriptor, name and mode
        ifname = ifname_bytes.decode('UTF-8')[:16].strip("\x00")  # Get Device Name

        self.name = ifname
        self.configured = False
        self.netmask_len = -1  # Initialize Value
        self.subnet = ''  # Initialize Value

    def configure(self, subnet, netmask_len):  # system configuration of device
        if type(netmask_len) != int:
            raise ValueError("'netmask_len' must be of type Integer, not %s." % type(netmask_len))
        if not (33 > netmask_len > 0):
            raise ValueError(
                "'netmask_len' value - '%d' is out of bounds, must be between 0 to 32." % netmask_len)

        self.subnet = subnet
        self.netmask_len = netmask_len

        # set up the tun interface
        os.system(
            "sudo ip addr add {}/{} dev {}".format(self.subnet, self.netmask_len, self.name))  # add address to device
        os.system("sudo ip link set dev {} up".format(self.name))  # set device 'up'
        self.configured = True

    def deconfigure(self):  # undoes system configuration at self.configure()
        if not self.configured:
            raise Exception('configure() must be used prior to deconfigure()')
        os.system("sudo ip addr del {}/{} dev {}".format(self.subnet, self.netmask_len, self.name))
        os.system("sudo ip link set dev {} down".format(self.name))

    def terminate(self):  # used at end of use
        os.close(self._file_descriptor)  # disables use of file descriptor, releasing related resources

    def read(self, bts):
        if type(bts) != int:
            raise ValueError("'bts' must be of type Integer, not %s." % type(bts))
        return os.read(self._file_descriptor, bts)

    def write(self, msg):
        if type(msg) != bytes:
            raise ValueError("'msg' must be of type Bytes, not %s." % type(msg))
        return os.write(self._file_descriptor, msg)

    def get_device(self):  # returning the file-descriptor
        return self._file_descriptor

    def __str__(self):
        return 'Flags: {}, Name: {}\nconfiguration: {}/{}'.format(hex(self.mode), self.name, self.subnet,
                                                                  self.netmask_len)

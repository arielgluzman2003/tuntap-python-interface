'''

Author: Arie Gluzman
Creation Date: 20.3.2021


'''

import os

INSERT = 'add'  # insert route entry
REMOVE = 'del'  # remove route entry


def set_route(operation, subnet, netmask, gateway, device):
    '''
    :param opera tion: Boolean, determines whether function is to add or to remove an entry
    :param subnet: String, destination subnet or address
    :param netmask: Integer, 0-32, destination subnet bytes used (32 if full address is given)
    :param gateway: String, address to which packet is to be routed
    :param device: String, device name to which packet is to be routed
    :return: None

    In essence, with parameters, the function constructs a string which it writes to OS Kernel
    root@user$ sudo route *operation* *subnet*/*netmask* gw*gateway* dev *device*
    e.g, root@user$ sudo route add 0.0.0.0/0 gw 192.168.1.1 dev enp0s3
    '''
    if type(operation) is not bool:
        raise ValueError("value must be of type 'bool', an argument of type {} was given".format(type(operation)))
    operation_text = REMOVE
    if operation:
        operation_text = INSERT
    print('sudo route {} {}/{} gw {} dev {}'.format(operation_text, subnet, netmask, gateway, device))
    os.system('sudo route {} {}/{} gw {} dev {}'.format(operation_text, subnet, netmask, gateway, device))

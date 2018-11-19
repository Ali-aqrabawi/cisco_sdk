import socket
import struct
import re


def clean_link_status(status):
    if 'down' in status:
        return 'down'
    if 'up' in status:
        return 'up'
    return 'unknown'


def translate_interface_name(name):
    """ Define shortcutting interface name """
    if 'tengigabitethernet' in name.lower():
        name = name.replace('TenGigabitEthernet', 'Te')
        return name

    if 'gigabitethernet' in name.lower():
        name = name.replace('GigabitEthernet', 'Gi')
        return name

    if 'fastethernet' in name.lower():
        name = name.replace('FastEthernet', 'Fa')
        return name

    if 'ethernet' in name.lower():
        name = name.replace('Ethernet', 'Eth')
        return name
    return name


def cidr_to_netmask(cidr):
    if not cidr:
        return None, None
    network, net_bits = cidr.split('/')
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return network, netmask


def exteract_software_version(descr):
    version = re.compile('Version ([0-9A-Za-z\(\)\.]*)')
    version = version.search(descr)
    if version:
        return version.group(1)
    return None


def extract_device_name(name):
    if '(' in name or '.' in name:
        match = re.search(r'^([^.(]+?)(\s*[.(])', name)
        if match:
            name = match.group(1)
    return name


def is_switchport(switch_port):
    if not switch_port:
        return False
    if 'no' in switch_port:
        return False
    return True

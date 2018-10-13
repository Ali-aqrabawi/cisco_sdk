"""
this module has the layer 2 config components ,
it has more business logic on the components like :
vlan.has_interface --> return true of that particular vlan has an interface
interface.is_svi --> return true of that particular interface is an svi interface
"""

from .base_component import FeatureSet, Feature
from cscmiko.features import utils


class Vlan(Feature):
    """single vlan model"""

    def __eq__(self, other):
        return isinstance(other, Vlan) and self.id == other.id

    @property
    def has_interface(self):
        if not self.interfaces:
            return False


class Vlans(FeatureSet):
    """
    device vlans manager class ,
    model attribute is to specify which model this class belong to
    """
    _feature_name = 'vlans'
    model = Vlan

    conf_template = "vlan.j2"


class Interface(Feature):
    """single interface model"""
    name: str
    link_status: str
    protocol_status: str
    hardware_type: str
    address: str
    ip_address: str
    mtu: int
    duplex: str
    speed: str
    bandwidth: int
    input_rate: int
    output_rate: int

    def __init__(self, int_dict):
        super().__init__(int_dict)
        cleand = []
        self.name = utils.translate_interface_name(self.name)
        self.link_status = utils.clean_link_status(self.link_status)
        self.protocol_status = utils.clean_link_status(self.protocol_status)
        self.mtu = int(self.mtu)
        self.bandwidth = int(self.bandwidth.replace(' Kbit', ''))
        self.input_rate = int(self.input_rate)
        self.output_rate = int(self.output_rate)
        self.ip_address, self.netmask = utils.cidr_to_netmask(self.ip_address)

    @property
    def is_svi(self):
        if self.hardware_type == 'EtherSVI':
            return True
        return False

    @property
    def is_port_channel(self):
        if self.hardware_type == 'EtherChannel':
            return True
        return False

    @property
    def is_loopback(self):
        if self.hardware_type == 'Loopback':
            return True
        return False

    @property
    def is_up(self):
        if self.link_status == 'up' and self.protocol_status == 'up':
            return True
        return False


class Interfaces(FeatureSet):
    """multiple interface models class"""
    _feature_name = 'interfaces'
    model = Interface
    conf_template = 'interface.j2'

    def bounce(self, id):
        self.cmds += [f"interface {id}", "shutdown", "no shutdown"]

    @property
    def down_list(self):
        return [i for i in self.all if not i.is_up]

    @property
    def svi_list(self):
        return [i for i in self.all if i.is_svi]

    @property
    def port_channel_list(self):
        return [i for i in self.all if i.is_port_channel]

    @property
    def loopback_list(self):
        return [i for i in self.all if i.is_loopback]


class CdpNrighbor(Feature):
    neighbor: str
    neighbor_ip: str
    platform: str
    remote_port: str
    local_port: str
    software_version: str

    def __init__(self, cdps):
        super().__init__(cdps)
        self.neighbor = utils.extract_device_name(self.neighbor)
        self.remote_port = utils.translate_interface_name(self.remote_port)
        self.local_port = utils.translate_interface_name(self.local_port)
        self.software_version = utils.exteract_software_version(self.software_version)


class CdpNeighbors(FeatureSet):
    _feature_name = 'cdp_neighbors'
    model = CdpNrighbor

    def get_cdps_for_port(self, port):
        return [i for i in self.all if i.local_port == port]

    def get_cdps_for_neighbor(self, neighbor_name):
        return [i for i in self.all if i.neighbor == neighbor_name]

    def get_cdp_by_ip(self, ip):
        return [i for i in self.all if i.neighbor_ip == ip]


class Vtp(Feature):
    pass


class Vpc(Feature):

    @property
    def is_up(self):
        if self.status == 'up':
            return True
        return False


class Vpcs(FeatureSet):
    model = Vpc
    _feature_name = 'vpcs'

    def get_vpc_by_port(self, port):
        return [i for i in self.all if i.port == port]


class Stp(Feature):
    pass


class Stps(FeatureSet):
    model = Stp
    _feature_name = 'spanning_tree'

    def get_by_vlan_id(self, id):
        return [stp for stp in self.all if stp.vlan_id == id]

    def get_by_interface(self, interface):
        for stp in self.all:
            if stp.interface == interface:
                return stp

    def get_by_port_status(self, status):
        """status = FWD|BLK"""
        return [stp for stp in self.all if stp.status == status]

    def get_blocked(self):
        return [stp for stp in self.all if stp.status == 'BLK']

    def get_forwarded(self):
        return [stp for stp in self.all if stp.status == 'FWD']

    def get_designated_ports(self):
        return [stp for stp in self.all if stp.status == 'Desg']

    def get_root_ports(self):
        return [stp for stp in self.all if stp.status == 'Root']

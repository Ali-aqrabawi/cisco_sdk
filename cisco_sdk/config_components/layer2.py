"""
this module has the layer 2 config components ,
it has more business logic on the components like :
vlan.has_interface --> return true of that particular vlan has an interface
interface.is_svi --> return true of that particular interface is an svi interface
"""

from .base_component import BaseConfigs, BaseConfig


class Vlan(BaseConfig):
    """single vlan model"""

    def __eq__(self, other):
        return isinstance(other, Vlan) and self.id == other.id

    @property
    def has_interface(self):
        if not self.interfaces:
            return False


class Vlans(BaseConfigs):
    """
    device vlans manager class ,
    model attribute is to specify which model this class belong to
    """
    model = Vlan

    conf_template = "vlan.j2"


class Interface(BaseConfig):
    """single interface model"""

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


class Interfaces(BaseConfigs):
    """multiple interface models class"""
    model = Interface

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


class CdpNeighbors(BaseConfigs):

    def get_cdps_for_port(self, port):
        return [i for i in self.all if i.local_port == port]

    def get_cdps_for_neighbor(self, neighbor_name):
        return [i for i in self.all if i.neighbor == neighbor_name]

    def get_cdp_by_ip(self, ip):
        return [i for i in self.all if i.neighbor_ip == ip]


class Vtp(BaseConfig):
    pass


class Vpc(BaseConfig):

    @property
    def is_up(self):
        if self.status == 'up':
            return True
        return False


class Vpcs(BaseConfigs):
    model = Vpc

    def get_vpc_by_port(self, port):
        return [i for i in self.all if i.port == port]

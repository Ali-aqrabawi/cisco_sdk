from .base import BaseConfigs,BaseConfig


class Vlan(BaseConfig):

    def __eq__(self, other):
        return isinstance(other, Vlan) and self.id == other.id

    @property
    def has_interface(self):
        if not self.interfaces:
            return False


class Vlans(BaseConfigs):
    model = Vlan


class Interface(BaseConfig):

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
    def is_up(self):
        if self.link_status == 'up' and self.protocol_status == 'up':
            return True
        return False


class Interfaces(BaseConfigs):
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


class CdpNeighbors(BaseConfigs):

    def get_cdps_for_port(self, port):
        return [i for i in self.all if i.local_port == port]

    def get_cdps_for_neighbor(self, neighbor_name):
        return [i for i in self.all if i.neighbor == neighbor_name]

    def get_cdp_by_ip(self, ip):
        return [i for i in self.all if i.neighbor_ip == ip]



class Vtp(BaseConfig):
    pass
"""
this module has the layer 3 config components ,
it has more business logic on the components like :
Route.is_eigrp --> return true of that particular route is eigrp route
BgpNeighbors.suppressed_list --> return list of suppressed bgp objects.
"""

from .base_component import Feature, FeatureSet
from . import utils


class Route(Feature):
    """single route feature"""
    protocol: str
    type: str
    network: str
    netmask: str
    distance: int
    metric: str
    nexthop_ip: str
    nexthop_interface: str
    uptime: str

    def __init__(self, output):
        super().__init__(output)
        self.protocol = utils.ROUTE_PROTOCOL.get(self.protocol, 'unknown')
        self.type = self.type or None
        self.network, self.netmask = utils.cidr_to_netmask(self.network + '/' + self.netmask)
        if self.distance is not None:
            self.distance = int(self.distance)
        if self.metric is not None:
            self.metric = int(self.metric)
        if self.nexthop_interface is not None:
            self.nexthop_interface = utils.translate_interface_name(self.nexthop_interface)

    @property
    def is_connected(self):
        return self.protocol == 'connected'

    @property
    def is_eigrp(self):
        return self.protocol == 'eigrp'

    @property
    def is_ospf(self):
        return self.protocol == 'ospf'

    @property
    def is_static(self):
        return self.protocol == 'static'

    @property
    def is_bgp(self):
        return self.protocol == 'bgp'

    @property
    def is_rip(self):
        return self.protocol == 'rip'


class Routes(FeatureSet):
    """FeatureSet : group of route Features"""
    model = Route
    _feature_name = 'routes'
    conf_template = 'route.j2'

    @property
    def ospf_list(self):
        return [i for i in self.all if i.is_ospf]

    @property
    def eigrp_list(self):
        return [i for i in self.all if i.is_eigrp]

    @property
    def direct_connected_list(self):
        return [i for i in self.all if i.is_connected]

    @property
    def static_list(self):
        return [i for i in self.all if i.is_static]

    @property
    def rip_list(self):
        return [i for i in self.all if i.is_rip]

    def get_routes_of_next_hope_ip(self, ip):
        return [i for i in self.all if ip == i.nexthop_ip]

    def get_routes_of_next_hope_if(self, interface):
        return [i for i in self.all if interface == i.nexthop_if.lower()]

    def get_routes_of_network(self, network):
        return [i for i in self.all if network == i.network]


class Bgp(Feature):
    """Bgp feature"""

    origin:str

    def __init__(self,output):
        super().__init__(output)
        if self.origin is not None:
            if self.is_egp_origin:
                self.origin = 'egp'
            elif self.is_igp_origin:
                self.origin = 'igp'
            elif self.is_incomplete:
                self.origin = 'incomplete'


    @property
    def is_igp_origin(self):
        if self.origin == 'i':
            return True
        return False

    @property
    def is_egp_origin(self):
        if self.origin == 'e':
            return True
        return False

    @property
    def is_incomplete(self):
        if self.origin == '?':
            return True
        return False

    @property
    def is_best(self):
        if self.path_selection == '<':
            return True
        return False

    @property
    def is_valid(self):
        if self.status == '*':
            return True
        return False

    @property
    def is_internal(self):
        if self.route_source == 'i':
            return True
        return False

    @property
    def is_suppressed(self):
        if self.status == 's':
            return True
        return False


class BgpNeighbors(FeatureSet):
    """FeatureSet: set of bgp Features"""
    model = Bgp
    _feature_name = 'bgp_neighbors'

    @property
    def suppressed_list(self):
        return [i for i in self.all if i.is_suppressed]

    @property
    def internal_list(self):
        return [i for i in self.all if i.is_internal]

    @property
    def valid_list(self):
        return [i for i in self.all if i.is_valid]

    @property
    def incomplete_list(self):
        return [i for i in self.all if i.is_incomplete]

    @property
    def best_list(self):
        return [i for i in self.all if i.is_best]

    @property
    def egp_list(self):
        return [i for i in self.all if i.is_egp]

    @property
    def igp_list(self):
        return [i for i in self.all if i.is_igp]

    def get_bgp_by_network(self, network):
        for i in self.all:
            if i.network == network:
                return i


class Ospf(Feature):
    """ospf neighbor Feature"""
    pass


class OspfNeighbors(FeatureSet):
    """FeatureSet: a set of ospf neighbors Feature"""
    model = Ospf
    _feature_name = 'ospf_neighbors'


class Vrf(Feature):
    """Vrf Feature"""
    pass


class Vrfs(FeatureSet):
    """FeatureSet: of vrfs Feature"""
    model = Vrf
    _feature_name = 'vrfs'

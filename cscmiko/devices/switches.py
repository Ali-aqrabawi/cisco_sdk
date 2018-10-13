"""
this module contain the devices managers, for different switch models (Cat,nexus ... etc)
device manager is the user interface to device , where you can fetch config components, push config , backup restore..etc
"""

from .base_device import CiscoDevice
from cscmiko.features import layer2, layer3, security, system
from abc import ABC
from cscmiko.exceptions import CscmikoNotSyncedError, CscmikoInvalidFeatureError

_INVETORY_CMD = "show version"
_VLAN_CMD = "show vlan"
_INTERFACE_CMD = "show interface"
_ROUTE_CMD = "show ip route"
_CDP_CMD = "show cdp neighbors detail"
_BGP_CMD = "show ip bgp"
_OSPF_CMD = "show ip ospf neighbor"
_ACL_CMD = "show ip access-list"
_VRF_CMD = "show vrf"
_VTP_CMD = "show vtp status"
_CPU_CMD = "show processes cpu"
_VPC_CMD = "show vpc"
_MODULE_CMD = "show module"
_STP_CMD = "show spanning-tree"


class _CiscoSwitch(CiscoDevice, ABC):
    """
    Base Cisco Switch manager ,
    this manager handle Cat switch config fetch , config push ,

    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.fetch_cpu_status()
    this example fetch CPU status , and set a cpu_status attibute for myswitch object
    """
    features_list = ['invetory', 'interfaces', 'vlans', 'cdp_neighbors', 'routes', 'access_lists', 'vtp_status',
                     'spanning_tree']

    def __getattr__(self, item):
        """
        this is only for raising CiscoSDKNotSyncedError, as the fetch method need to be called before accessing the
        config attribute (e.g. myswitch.vlans )

        for every config compnent(vlans,vrfs,interfaces ... etc) we have a fetch method listed below ,
        :param item: attribute
        :return:
        """
        if item not in self.features_list:
            raise CscmikoInvalidFeatureError(
                f"{item.replace('fetch_','')} is not a valid feature , available features = {self.features_list}")
        if not item.endswith('s'):
            item = item + 's'
        raise CscmikoNotSyncedError(
            f"{item} is not collected  please make sure to call fetch_{item} before, available features : {self.features_list}")

    # Sync Methods
    # TODO : make the add fetch to base class to have a reusable fetch code

    def fetch_inventory(self):
        print(f"Collecting Inventory details from {self.host} ...")
        inventory_dict = self.get_command_output(_INVETORY_CMD)
        if not inventory_dict:
            print("No inventory details collected")
            return None
        self.inventory = system.Inventory(inventory_dict[0])

    # layer 2 fetch methods
    def fetch_interfaces(self):
        print(f"Collecting Interfaces from {self.host} ...")
        interfaces_dicts = self.get_command_output(_INTERFACE_CMD)
        if not interfaces_dicts:
            print("No interfaces collected")
            return None
        self.interfaces = layer2.Interfaces(interfaces_dicts)

    def fetch_vlans(self):
        print(f"Collecting Vlans from {self.host} ...")
        vlans_dicts = self.get_command_output(_VLAN_CMD)
        if not vlans_dicts:
            print("No vlans collected")
            return None
        self.vlans = layer2.Vlans(vlans_dicts)

    def fetch_cdp_neighbors(self):
        print(f"Collecting CDP neighbors from {self.host} ...")
        cdps_dicts = self.get_command_output(_CDP_CMD)
        if not cdps_dicts:
            print("No cdp neighbors collected")
            return None
        self.cdp_neighbors = layer2.CdpNeighbors(cdps_dicts)

    # Layer 3 fetch methods
    def fetch_routes(self):
        print(f"Collecting Routes from {self.host} ...")
        routes_dicts = self.get_command_output(_ROUTE_CMD)
        if not routes_dicts:
            print("No Routes collected")
            return None
        self.routes = layer3.Routes(routes_dicts)

    # security fetch methods
    def fetch_access_lists(self):
        print(f"Collecting access-lists from {self.host} ...")
        acls_dicts = self.get_command_output(_ACL_CMD)
        if not acls_dicts:
            print("No acls collected")
            self.access_lists = None
            return None
        self.access_lists = security.AccessLists(acls_dicts)

    def fetch_spanning_tree(self):
        print(f"Collecting spanning-tree from {self.host} ...")
        stp_dict = self.get_command_output(_STP_CMD)
        if not stp_dict:
            print("No stp collected")
            self.spanning_tree = None
            return None
        self.spanning_tree = layer2.Stps(stp_dict)

    def fetch_vtp_status(self):
        print(f"Collecting vtp status from {self.host} ...")
        vtp_dicts = self.get_command_output(_VTP_CMD)
        if not vtp_dicts:
            print("No vlans collected")
            return None
        self.vtp_status = layer2.Vtp(vtp_dicts[0])

    def fetch(self):
        """
        this call all the fetch_methods incase you want to fetch all components ,
        :return:
        """

        self.fetch_interfaces()
        self.fetch_vlans()
        self.fetch_spanning_tree()
        self.fetch_cdp_neighbors()
        self.fetch_routes()
        self.fetch_access_lists()
        self.fetch_vtp_status()


class CatSwitch(_CiscoSwitch):
    """
    Catalyst Switch device manager which hold it's own fetch methods in addition to base CiscoDevice fetch methods
    """
    device_type = 'cisco_ios'
    features_list = _CiscoSwitch.features_list + ['fetch_cpu_status', 'bgp_neighbors', 'ospf_neighbors', 'vrfs']

    def fetch_cpu_status(self):
        print(f"Collecting cpu status from {self.host} ...")
        cpu_dict = self.get_command_output(_CPU_CMD)
        if not cpu_dict:
            print("No cpu status collected")
            return None
        self.cpu_status = system.Cpu(cpu_dict[0])

    def fetch_bgp_neighbors(self):
        print(f"Collecting BGP neighbors from {self.host} ...")
        bgps_dicts = self.get_command_output(_BGP_CMD)
        if not bgps_dicts:
            print("No BGP collected")
            self.bgp_neighbors = None
            return None
        self.bgp_neighbors = layer3.BgpNeighbors(bgps_dicts)

    def fetch_ospf_neighbors(self):
        print(f"Collecting OSPF neighbors from {self.host} ...")
        ospfs_dicts = self.get_command_output(_OSPF_CMD)
        if not ospfs_dicts:
            print("No OSPF collected")
            self.ospf_neighbors = None
            return None
        self.ospf_neighbors = layer3.OspfNeighbors(ospfs_dicts)

    def fetch_vrfs(self):
        print(f"Collecting VRFs from {self.host} ...")
        vrfs_dicts = self.get_command_output(_VRF_CMD)
        if not vrfs_dicts:
            print("No VRFS collected")
            self.vrfs = None
            return None
        self.vrfs = layer3.Vrfs(vrfs_dicts)

    def fetch(self):
        super().fetch()
        self.fetch_cpu_status()
        self.fetch_ospf_neighbors()
        self.fetch_bgp_neighbors()
        self.fetch_vrfs()


class NexusSwitch(_CiscoSwitch):
    """
    Nexus 9K and 7k Switch device manager which hold it's own fetch methods in addition to base CiscoDevice fetch methods
    """
    device_type = 'cisco_nxos'
    features_list = _CiscoSwitch.features_list + ['modules', 'vpcs']

    def fetch_modules(self):
        print(f"Collecting Modules from {self.host} ...")
        modules_dicts = self.get_command_output(_VRF_CMD)
        if not modules_dicts:
            print("No Modules collected")
            self.modules = None
            return None
        self.modules = system.Modules(modules_dicts)

    def fetch_vpc(self):
        print(f"Collecting vpcs from {self.host} ...")
        vpc_dicts = self.get_command_output(_VPC_CMD)
        if not vpc_dicts:
            print("No vpcs collected")
            self.modules = None
            return None
        self.vpcs = layer2.Vpcs(vpc_dicts)

    def fetch(self):
        super().fetch()
        self.fetch_modules()
        self.fetch_vpc()

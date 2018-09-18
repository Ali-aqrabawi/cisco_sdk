"""
this module contain the devices managers, for different switch models (Cat,nexus ... etc)
device manager is the user interface to device , where you can sync config components, push config , backup restore..etc
"""

from .base_device import CiscoDevice
from cscmiko.features import layer2, layer3, security, system
from abc import ABC
from cscmiko.exceptions import CscmikoNotSyncedError, CscmikoInvalidFeatureError

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
    this manager handle Cat switch config sync , config push ,

    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.sync_cpu_status()
    this example sync CPU status , and set a cpu_status attibute for myswitch object
    """
    features_list = ['interfaces', 'vlans', 'cdp_neighbors', 'routes', 'access_lists', 'vtp_status', 'spanning_tree']

    def __getattr__(self, item):
        """
        this is only for raising CiscoSDKNotSyncedError, as the sync method need to be called before accessing the
        config attribute (e.g. myswitch.vlans )

        for every config compnent(vlans,vrfs,interfaces ... etc) we have a sync method listed below ,
        :param item: attribute
        :return:
        """
        if item not in self.features_list:
            raise CscmikoInvalidFeatureError(
                f"{item.replace('sync_','')} is not a valid feature , available features = {self.features_list}")
        if not item.endswith('s'):
            item = item + 's'
        raise CscmikoNotSyncedError(
            f"{item} is not synced  please make sure to call sync_{item} before, available features : {self.features_list}")

    # Sync Methods
    # TODO : make the add sync to base class to have a reusable sync code

    # layer 2 sync methods
    def sync_interfaces(self):
        print(f"Collecting Interfaces from {self.host} ...")
        interfaces_dicts = self.get_command_output(_INTERFACE_CMD)
        if not interfaces_dicts:
            print("No interfaces collected")
            return None
        self.interfaces = layer2.Interfaces(interfaces_dicts)

    def sync_vlans(self):
        print(f"Collecting Vlans from {self.host} ...")
        vlans_dicts = self.get_command_output(_VLAN_CMD)
        if not vlans_dicts:
            print("No vlans collected")
            return None
        self.vlans = layer2.Vlans(vlans_dicts)

    def sync_cdp_neighbors(self):
        print(f"Collecting CDP neighbors from {self.host} ...")
        cdps_dicts = self.get_command_output(_CDP_CMD)
        if not cdps_dicts:
            print("No cdp neighbors collected")
            return None
        self.cdp_neighbors = layer2.CdpNeighbors(cdps_dicts)

    # Layer 3 sync methods
    def sync_routes(self):
        print(f"Collecting Routes from {self.host} ...")
        routes_dicts = self.get_command_output(_ROUTE_CMD)
        if not routes_dicts:
            print("No Routes collected")
            return None
        self.routes = layer3.Routes(routes_dicts)

    # security sync methods
    def sync_access_lists(self):
        print(f"Collecting access-lists from {self.host} ...")
        acls_dicts = self.get_command_output(_ACL_CMD)
        if not acls_dicts:
            print("No acls collected")
            self.access_lists = None
            return None
        self.access_lists = security.AccessLists(acls_dicts)

    def sync_spanning_tree(self):
        print(f"Collecting spanning-tree from {self.host} ...")
        stp_dict = self.get_command_output(_STP_CMD)
        if not stp_dict:
            print("No stp collected")
            self.spanning_tree = None
            return None
        self.spanning_tree = layer2.Stps(stp_dict)

    def sync_vtp_status(self):
        print(f"Collecting vtp status from {self.host} ...")
        vtp_dicts = self.get_command_output(_VTP_CMD)
        if not vtp_dicts:
            print("No vlans collected")
            return None
        self.vtp_status = layer2.Vtp(vtp_dicts[0])

    def sync(self):
        """
        this call all the sync_methods incase you want to sync all components ,
        :return:
        """

        self.sync_interfaces()
        self.sync_vlans()
        self.sync_spanning_tree()
        self.sync_cdp_neighbors()
        self.sync_routes()
        self.sync_access_lists()
        self.sync_vtp_status()


class CatSwitch(_CiscoSwitch):
    """
    Catalyst Switch device manager which hold it's own sync methods in addition to base CiscoDevice sync methods
    """
    device_type = 'cisco_ios'
    features_list = _CiscoSwitch.features_list + ['sync_cpu_status', 'bgp_neighbors', 'ospf_neighbors', 'vrfs']

    def sync_cpu_status(self):
        print(f"Collecting cpu status from {self.host} ...")
        cpu_dict = self.get_command_output(_CPU_CMD)
        if not cpu_dict:
            print("No cpu status collected")
            return None
        self.cpu_status = system.Cpu(cpu_dict[0])

    def sync_bgp_neighbors(self):
        print(f"Collecting BGP neighbors from {self.host} ...")
        bgps_dicts = self.get_command_output(_BGP_CMD)
        if not bgps_dicts:
            print("No BGP collected")
            self.bgp_neighbors = None
            return None
        self.bgp_neighbors = layer3.BgpNeighbors(bgps_dicts)

    def sync_ospf_neighbors(self):
        print(f"Collecting OSPF neighbors from {self.host} ...")
        ospfs_dicts = self.get_command_output(_OSPF_CMD)
        if not ospfs_dicts:
            print("No OSPF collected")
            self.ospf_neighbors = None
            return None
        self.ospf_neighbors = layer3.OspfNeighbors(ospfs_dicts)

    def sync_vrfs(self):
        print(f"Collecting VRFs from {self.host} ...")
        vrfs_dicts = self.get_command_output(_VRF_CMD)
        if not vrfs_dicts:
            print("No VRFS collected")
            self.vrfs = None
            return None
        self.vrfs = layer3.Vrfs(vrfs_dicts)

    def sync(self):
        super().sync()
        self.sync_cpu_status()
        self.sync_ospf_neighbors()
        self.sync_bgp_neighbors()
        self.sync_vrfs()


class NexusSwitch(_CiscoSwitch):
    """
    Nexus 9K and 7k Switch device manager which hold it's own sync methods in addition to base CiscoDevice sync methods
    """
    device_type = 'cisco_nxos'
    features_list = _CiscoSwitch.features_list + ['modules', 'vpcs']

    def sync_modules(self):
        print(f"Collecting Modules from {self.host} ...")
        modules_dicts = self.get_command_output(_VRF_CMD)
        if not modules_dicts:
            print("No Modules collected")
            self.modules = None
            return None
        self.modules = system.Modules(modules_dicts)

    def sync_vpc(self):
        print(f"Collecting vpcs from {self.host} ...")
        vpc_dicts = self.get_command_output(_VPC_CMD)
        if not vpc_dicts:
            print("No vpcs collected")
            self.modules = None
            return None
        self.vpcs = layer2.Vpcs(vpc_dicts)

    def sync(self):
        super().sync()
        self.sync_modules()
        self.sync_vpc()

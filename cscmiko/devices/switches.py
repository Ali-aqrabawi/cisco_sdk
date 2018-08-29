"""
this module contain the devices managers, for different switch models (Cat,nexus ... etc)
device manager is the user interface to device , where you can sync config components, push config , backup restore..etc
"""

from .base_device import CiscoDevice
from cscmiko.features import layer2, layer3, security, system
from abc import ABC
from cscmiko.exceptions import CiscoSDKNotSyncedError

VLAN_CMD = "show vlan"
INTERFACE_CMD = "show interface"
ROUTE_CMD = "show ip route"
CDP_CMD = "show cdp neighbors detail"
BGP_CMD = "show ip bgp"
OSPF_CMD = "show ip ospf neighbor"
ACL_CMD = "show ip access-list"
VRF_CMD = "show vrf"
VTP_CMD = "show vtp status"
CPU_CMD = "show processes cpu"
VPC_CMD = "show vpc"
MODULE_CMD = "show module"


class CiscoSwitch(CiscoDevice, ABC):
    """
    Base Cisco Switch manager ,
    this manager handle Cat switch config sync , config push ,

    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.sync_cpu_status()
    this example sync CPU status , and set a cpu_status attibute for myswitch object
    """

    def __getattr__(self, item):
        """
        this is only for raising CiscoSDKNotSyncedError, as the sync method need to be called before accessing the
        config attribute (e.g. myswitch.vlans )

        for every config compnent(vlans,vrfs,interfaces ... etc) we have a sync method listed below ,
        :param item: attribute
        :return:
        """
        if not item.endswith('s'):
            item = item + 's'
        raise CiscoSDKNotSyncedError(f"{item} is not synced  please make sure to call sync_{item} before,")

    # Sync Methods
    # TODO : make the add sync to base class to have a reusable sync code
    # TODO : sync methods shouldn't call get_command(cmd), it should take lists_dicts as arg , and set the attr
    # layer 2 sync methods
    def sync_interfaces(self):
        print(f"Collecting Interfaces from {self.connection_dict['ip']} ...")
        interfaces_dicts = self.get_command_output(INTERFACE_CMD)
        if not interfaces_dicts:
            print("No interfaces collected")
            return None
        self.interfaces = layer2.Interfaces(interfaces_dicts)

    def sync_vlans(self):
        print(f"Collecting Vlans from {self.connection_dict['ip']} ...")
        vlans_dicts = self.get_command_output(VLAN_CMD)
        if not vlans_dicts:
            print("No vlans collected")
            return None
        self.vlans = layer2.Vlans(vlans_dicts)

    def sync_cdp_neighbors(self):
        print(f"Collecting CDP neighbors from {self.connection_dict['ip']} ...")
        cdps_dicts = self.get_command_output(CDP_CMD)
        if not cdps_dicts:
            print("No cdp neighbors collected")
            return None
        self.cdp_neighbors = layer2.CdpNeighbors(cdps_dicts)

    # Layer 3 sync methods
    def sync_routes(self):
        print(f"Collecting Routes from {self.connection_dict['ip']} ...")
        routes_dicts = self.get_command_output(ROUTE_CMD)
        if not routes_dicts:
            print("No Routes collected")
            return None
        self.routes = layer3.Routes(routes_dicts)

    # security sync methods
    def sync_access_lists(self):
        print(f"Collecting access-lists from {self.connection_dict['ip']} ...")
        acls_dicts = self.get_command_output(ACL_CMD)
        if not acls_dicts:
            print("No acls collected")
            self.access_lists = None
            return None
        self.access_lists = security.AccessLists(acls_dicts)

    def sync_vtp_status(self):
        print(f"Collecting vtp status from {self.connection_dict['ip']} ...")
        vtp_dicts = self.get_command_output(VTP_CMD)
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
        self.sync_cdp_neighbors()
        self.sync_routes()
        self.sync_access_lists()
        self.sync_vtp_status()


class CatSwitch(CiscoSwitch):
    """
    Catalyst Switch device manager which hold it's own sync methods in addition to base CiscoDevice sync methods
    """
    device_type = 'cisco_ios'

    def sync_cpu_status(self):
        print(f"Collecting cpu status from {self.connection_dict['ip']} ...")
        cpu_dict = self.get_command_output(CPU_CMD)
        if not cpu_dict:
            print("No cpu status collected")
            return None
        self.cpu_status = system.Cpu(cpu_dict[0])

    def sync_bgp_neighbors(self):
        print(f"Collecting BGP neighbors from {self.connection_dict['ip']} ...")
        bgps_dicts = self.get_command_output(BGP_CMD)
        if not bgps_dicts:
            print("No BGP collected")
            self.bgp_neighbors = None
            return None
        self.bgp_neighbors = layer3.BgpNeighbors(bgps_dicts)

    def sync_ospf_neighbors(self):
        print(f"Collecting OSPF neighbors from {self.connection_dict['ip']} ...")
        ospfs_dicts = self.get_command_output(OSPF_CMD)
        if not ospfs_dicts:
            print("No OSPF collected")
            self.ospf_neighbors = None
            return None
        self.ospf_neighbors = layer3.OspfNeighbors(ospfs_dicts)

    def sync_vrfs(self):
        print(f"Collecting VRFs from {self.connection_dict['ip']} ...")
        vrfs_dicts = self.get_command_output(VRF_CMD)
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


class NexusSwitch(CiscoSwitch):
    """
    Nexus 9K and 7k Switch device manager which hold it's own sync methods in addition to base CiscoDevice sync methods
    """
    device_type = 'cisco_nxos'

    def sync_modules(self):
        print(f"Collecting Modules from {self.connection_dict['ip']} ...")
        modules_dicts = self.get_command_output(VRF_CMD)
        if not modules_dicts:
            print("No Modules collected")
            self.modules = None
            return None
        self.modules = system.Modules(modules_dicts)

    def sync_vpc(self):
        print(f"Collecting vpcs from {self.connection_dict['ip']} ...")
        vpc_dicts = self.get_command_output(VPC_CMD)
        if not vpc_dicts:
            print("No vpcs collected")
            self.modules = None
            return None
        self.vpcs = layer2.Vpcs(vpc_dicts)

    def sync(self):
        super().sync()
        self.sync_modules()
        self.sync_vpc()

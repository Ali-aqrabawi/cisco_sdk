from cscmiko.devices.base.device import Device
from cscmiko.models import layer2, layer3, security, system
from abc import ABC
from cscmiko.exceptions import CscmikoNotSyncedError, CscmikoInvalidFeatureError

_INVETORY_CMD = "show version"
_VLAN_CMD = "show vlan"
_INTERFACE_CMD = "show interface"
_INTERFACE_CONF_CMD = "show run | section interface"
_ROUTE_CMD = "show ip route"
_CDP_CMD = "show cdp neighbors detail"
_BGP_CMD = "show ip bgp"
_OSPF_CMD = "show ip ospf neighbor"
_ACL_CMD = "show ip access-list"
_VRF_CMD = "show vrf"
_VTP_CMD = "show vtp status"
_CPU_CMD = "show processes cpu"
_MEM_CMD = "show processes memory"
_VPC_CMD = "show vpc"
_MODULE_CMD = "show module"
_STP_CMD = "show spanning-tree"


class _CiscoSwitch(Device, ABC):
    """
    Base Cisco Switch manager ,
    this manager handle Cat switch config fetch , config push ,

    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.fetch_cpu_status()
    this example fetch CPU status , and set a cpu_status attibute for myswitch object
    """
    features_list = ['inventory', 'interfaces', 'vlans', 'cdp_neighbors', 'routes', 'access_lists', 'vtp_status',
                     'spanning_tree', 'interfaces_configs']

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
                f"{item.replace('fetch_','')} is not a valid feature , available models = {self.features_list}")
        if not item.endswith('s'):
            item = item + 's'
        raise CscmikoNotSyncedError(
            f"{item} is not collected  please make sure to call fetch_{item} before, available models : {self.features_list}")

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

    def fetch_interfaces_configs(self):
        print(f"Collecting Interfaces configs from {self.host} ...")
        interfaces_configs_dicts = self.get_command_output(_INTERFACE_CONF_CMD)
        if not interfaces_configs_dicts:
            print("No interfaces config collected")
            return None
        self.interfaces_configs = layer2.InterfaceConfigs(interfaces_configs_dicts)

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

    def fetch_lldp_neighbors(self):
        print(f"Collecting LLDP neighbors from {self.host} ...")
        lldps_dicts = self.get_command_output(_CDP_CMD)
        if not lldps_dicts:
            print("No LLDP neighbors collected")
            return None
        self.lldp_neighbors = layer2.LldpNeighbors(lldps_dicts)

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

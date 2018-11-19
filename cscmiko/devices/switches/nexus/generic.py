from cscmiko.devices.switches.base import _CiscoSwitch
from cscmiko.models import system, layer2

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

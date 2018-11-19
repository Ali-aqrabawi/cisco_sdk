from cscmiko.devices.switches.base import _CiscoSwitch
from cscmiko.models import layer3, system


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


class CatSwitch(_CiscoSwitch):
    """
    Catalyst Switch device manager which hold it's own fetch methods in addition to base CiscoDevice fetch methods
    """
    device_type = 'cisco_ios'
    features_list = _CiscoSwitch.features_list + ['cpu_status', 'memory_status', 'bgp_neighbors', 'ospf_neighbors',
                                                  'vrfs']

    def fetch_cpu_status(self):
        print(f"Collecting cpu status from {self.host} ...")
        cpu_dict = self.get_command_output(_CPU_CMD)
        if not cpu_dict:
            print("No cpu status collected")
            return None
        self.cpu_status = system.Cpu(cpu_dict[0])

    def fetch_memory_status(self):
        print(f"Collecting memory status from {self.host} ...")
        mem_dict = self.get_command_output(_MEM_CMD)
        if not mem_dict:
            print("No cpu status collected")
            return None
        self.memory_status = system.Memory(mem_dict[0])

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

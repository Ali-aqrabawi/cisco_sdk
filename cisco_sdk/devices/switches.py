from .baseClass import CiscoDevice
from cisco_sdk.config_components import layer2, layer3, security, system

VLAN_CMD = "show vlan"
INTERFACE_CMD = "show interfaces"
ROUTE_CMD = "show ip route"
CDP_CMD = "show cdp neighbors detail"
BGP_CMD = "show ip bgp"
OSPF_CMD = "show ip ospf neighbor"
ACL_CMD = "show ip access-list"
VRF_CMD = "show vrf"
VTP_CMD = "show vtp status"
CPU_CMD = "show processes cpu"


class CiscoSDKNotSyncedError(Exception):
    pass


class CatSwitch(CiscoDevice):
    device_type = "cisco_ios"

    def __getattr__(self, item):
        if not item.endswith('s'):
            item = item + 's'
        raise CiscoSDKNotSyncedError(f"{item} is not synced , please make sure to call sync_{item} before,")

    # system sync methods
    def sync_cpu_status(self):
        print(f"Collecting cpu status from {self.connection_dict['ip']} ...")
        cpu_dict = self.get_command(CPU_CMD)
        if not cpu_dict:
            print("No cpu status collected")
            return None
        self.cpu_status = system.Cpu(cpu_dict[0])

    # layer 2 sync methods
    def sync_interfaces(self):
        print(f"Collecting Interfaces from {self.connection_dict['ip']} ...")
        interfaces_dicts = self.get_command(INTERFACE_CMD)
        if not interfaces_dicts:
            print("No interfaces collected")
            return None
        self.interfaces = layer2.Interfaces(interfaces_dicts)

    def sync_vlans(self):
        print(f"Collecting Vlans from {self.connection_dict['ip']} ...")
        vlans_dicts = self.get_command(VLAN_CMD)
        if not vlans_dicts:
            print("No vlans collected")
            return None
        self.vlans = layer2.Vlans(vlans_dicts)

    def sync_vtp_status(self):
        print(f"Collecting vtp status from {self.connection_dict['ip']} ...")
        vtp_dicts = self.get_command(VTP_CMD)
        if not vtp_dicts:
            print("No vlans collected")
            return None
        self.vtp_status = layer2.Vtp(vtp_dicts[0])

    def sync_cdp_neighbors(self):
        print(f"Collecting CDP neighbors from {self.connection_dict['ip']} ...")
        cdps_dicts = self.get_command(CDP_CMD)
        if not cdps_dicts:
            print("No cdp neighbors collected")
            return None
        self.cdp_neighbors = layer2.CdpNeighbors(cdps_dicts)

    # Layer 3 sync methods
    def sync_routes(self):
        print(f"Collecting Routes from {self.connection_dict['ip']} ...")
        routes_dicts = self.get_command(ROUTE_CMD)
        if not routes_dicts:
            print("No Routes collected")
            return None
        self.routes = layer3.Routes(routes_dicts)

    def sync_bgp_neighbors(self):
        print(f"Collecting BGP neighbors from {self.connection_dict['ip']} ...")
        bgps_dicts = self.get_command(BGP_CMD)
        if not bgps_dicts:
            print("No BGP collected")
            self.bgp_neighbors = None
            return None
        self.bgp_neighbors = layer3.BgpNeighbors(bgps_dicts)

    def sync_ospf_neighbors(self):
        print(f"Collecting OSPF neighbors from {self.connection_dict['ip']} ...")
        ospfs_dicts = self.get_command(OSPF_CMD)
        if not ospfs_dicts:
            print("No OSPF collected")
            self.ospf_neighbors = None
            return None
        self.ospf_neighbors = layer3.OspfNeighbors(ospfs_dicts)

    def sync_vrfs(self):
        print(f"Collecting VRFs from {self.connection_dict['ip']} ...")
        vrfs_dicts = self.get_command(VRF_CMD)
        if not vrfs_dicts:
            print("No VRFS collected")
            self.vrfs = None
            return None
        self.vrfs = layer3.Vrfs(vrfs_dicts)

    # security sync methods
    def sync_access_lists(self):
        print(f"Collecting access-lists from {self.connection_dict['ip']} ...")
        acls_dicts = self.get_command(ACL_CMD)
        if not acls_dicts:
            print("No acls collected")
            self.access_lists = None
            return None
        self.access_lists = security.AccessLists(acls_dicts)

    def sync(self):
        self.sync_cpu_status()
        self.sync_interfaces()
        self.sync_vlans()
        self.sync_vtp_status()
        self.sync_cdp_neighbors()

        self.sync_routes()
        self.sync_bgp_neighbors()
        self.sync_ospf_neighbors()
        self.sync_vrfs()

        self.sync_access_lists()

from cscmiko.devices import CatSwitch

my_swicth = CatSwitch(host='192.168.1.1', username='admin', password='admin')

my_swicth.sync_spanning_tree()

# list of stp  for vlan 52 with Designated ports
stp_vlan51_ = my_swicth.spanning_tree.filter(vlan_id='52', role='Desg')

blk_stps = my_swicth.interfaces_stps.get_blocked()
frd_stps = my_swicth.interfaces_stps.get_forwarded()
root_pots = my_swicth.interfaces_stps.get_root_ports()
destinated_ports = my_swicth.interfaces_stps.get_designated_ports()

from cscmiko.devices import CatSwitch


acl = {
    "name": "test",
    "type": "extended",
    "rules": [
        {
            "action": "permit",
            "protocol": "udp",
            "src": "10.10.9.9",
            "src_wc": "",  # leave it empty if you want to match host
            "src_port_match": "",
            "src_ports": [],
            "dest": "20.20.20.9",
            "dest_wc": "",
            "dest_port_match": "eq",
            "dest_port": ['44', '8080']

        },
        {
            "action": "deny",
            "protocol": "tcp",
            "src": "10.10.9.9",
            "src_wc": "",  # leave it empty if you want to match host
            "src_port_match": "",
            "src_ports": [],
            "dest": "20.20.20.9",
            "dest_wc": "",
            "dest_port_match": "eq",
            "dest_ports": ['70', '8080']

        },

    ]

}
my_swicth = CatSwitch(host='192.168.1.1', username='admin', password='admin')
my_swicth.sync_access_lists()


my_swicth.access_lists.delete(**acl)
for cmd in my_swicth.access_lists.cmds:
    print(cmd)
is_ok,msg = my_swicth.commit(save=True)
print(is_ok)

"""
results :
    Collecting access-lists from 192.168.1.1 ...
    connecting to 192.168.1.1
    connecting to 192.168.1.1
    ip access-list extended test
    permit udp host 10.10.9.9    host 20.20.20.9
    deny tcp host 10.10.9.9    host 20.20.20.9   eq  70  8080
    True
"""
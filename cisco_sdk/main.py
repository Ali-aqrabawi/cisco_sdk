from cisco_sdk.devices.switches import CatSwitch

my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='admin')

my_swicth.sync_interfaces()


for i in my_swicth.interfaces:
    print(i.name , " is " , i.link_status)
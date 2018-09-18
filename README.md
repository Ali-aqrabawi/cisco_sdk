# cscmiko SDK

SDK for cisco Catalyst , Nexus, ASA, wireless lan controllers, built using Netmiko and ntc-templates,

### Installing

1. download [templates](https://github.com/Ali-aqrabawi/cscmiko) folder and place it at `~/ntc-tempalates/templates`
2. `pip install cscmiko`

### Getting Started

#### Example 1:

to get interfaces from the device:

    from cscmiko.devices import CatSwitch
    my_switch = CatSwitch(host='192.168.1.1', username='admin', password='admin')
    my_switch.sync_interfaces()

    for interface in my_switch.interfaces :
        print(interface.name , " is " , interface.link_status)

results :

    GigabitEthernet1/1/1  is  administratively down
    GigabitEthernet1/1/2  is  administratively down
    GigabitEthernet1/1/3  is  administratively down
    TenGigabitEthernet1/1/4  is  up
    TenGigabitEthernet1/1/5  is  up
    TenGigabitEthernet1/2/1  is  down
    TenGigabitEthernet1/2/2  is  up

you can also filter:

    filtered = my_switch.filter(status = 'down')  # return list of down interfaces objects

#### Example 2:
to add a VLAN to the device:

    from cscmiko.devices import CatSwitch
    my_switch = CatSwitch(host='192.168.1.1', username='admin', password='admin')
    my_switch.sync_vlans()
    my_switch.vlans.add(id='911', name="Vlan911")
    is_ok, msgs = my_switch.commit()
    print(is_ok)


results:

    True


#### Example 3:
Nexus switch

    from cscmiko.devices import NexusSwitch
    my_switch = NexusSwitch(host='192.168.1.2', username='admin', password='admin')
    my_switch.sync_vpc()

    print("list of up VPCs :")
    for vpc in my_switch.vpcs:
        if vpc.is_up:
            print("id:",vpc.id,"- port: ",vpc.port)

results:

    list of up VPCs :
    id: 1 - port:  Po99

### Contributing

Please read [CONTRIBUTING.md](https://github.com/Ali-aqrabawi/cscmiko/blob/master/CONTRIBUTION.md)  for details on our code of conduct, and the process for submitting pull requests to us.
# Cisco SDK

SDK for cisco devices build using Netmiko and ntc-templates,

### Installing
 1) download [templats](https://github.com/Ali-aqrabawi/cisco_sdk) folder and place it
 at `~/ntc-tempalates/templates`
  2) `pip install cisco_sdk`

### Getting Started
    from cisco_sdk.devices.switches import CatSwitch
    my_swicth = CatSwitch(host='192.168.1.1', username='admin', password='admin')
    my_swicth.sync_interfaces()

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

### Contributing

Please read [CONTRIBUTING.md](https://github.com/Ali-aqrabawi/cisco_sdk/blob/master/CONTRIBUTION.md)  for details on our code of conduct, and the process for submitting pull requests to us.
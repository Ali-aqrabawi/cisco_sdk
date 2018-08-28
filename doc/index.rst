$cisco_sdk
========

cisco_sdk is an sdk that uses netmiko to provide a high level API for network automation.

$Example 1:

to sync interfaces from the device:
.. code-block:: python
    from cisco_sdk.devices.switches import CatSwitch
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

.. note:: ``my_switch`` object get the features(vlans, interfaces,routes ... etc) attributes dynamicaly,
            so you can't access ``my_switch.vlans`` before calling ``.sync_interfaces()``, also please note that
            ``.interfaces`` attribute has properties like (``admin_status``,``id``,``ip_address`` ... etc) see `feature_list`_ for all
            available properties .
..`feature_list`_ https://cisco-sdk.readthedocs.io/en/latest/feature_list.rst
Example 2:
to add a Vlan to the device:
.. code-block:: python
    from cisco_sdk.devices.switches import CatSwitch
    my_swicth = CatSwitch(host='192.168.1.1', username='admin', password='admin')
    my_swicth.sync_vlans()
    my_swicth.vlans.add(id='911', name="Vlan911")
    is_ok, msgs = my_swicth.commit()
    print(is_ok)


results:

    True


Example 3:
Nexus switch
.. code-block:: python
    from cisco_sdk.devices.switches import NexusSwitch
    my_swicth = NexusSwitch(host='192.168.1.2', username='admin', password='admin')
    my_swicth.sync_vpc()

    print("list of up VPCs :")
    for vpc in my_swicth.vpcs:
        if vpc.is_up:
            print("id:",vpc.id,"- port: ",vpc.port)

results:

    list of up VPCs :
    id: 1 - port:  Po99

Features
--------

$cisco_sdk support following devices:

* Catalyst switches
* Nexus switches
* WLC
* Firewall

cisco_sdk support :

* sync fetching config from device and modeling the data so it can be easy accessed link ``my_switch.routes.all`` return
  all the routes.
* pushing config to devices, the devices API will validate if the config is successfully applied on the device or not.
* management operations like (backup, restore, ping, traceroute, reboot)

Installation
------------

Install cisco_sdk by running:

    pip install cisco_sdk


Support
-------

If you are having issues, please open issue on the `project repository`_
you can send you questions to : ali_aqrabawi@yahoo.com
.. _project repository: https://github.com/Ali-aqrabawi/cisco_sdk
License
-------

The project is licensed under the MIT license.
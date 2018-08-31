from cscmiko.devices.switches import CatSwitch


def print_routes(routes):
    for route in routes:
        print('###################')
        print("network = %s" % route.network)
        print("nprotocol = %s" % route.protocol)
        print("next_hope = %s" % route.nexthop_ip or route.nexthop_int)


def main():
    """ Example of synchronizing routes from device, adding static route and delelting it"""
    my_swicth = CatSwitch(host='192.168.1.1', username='admin', password='admin')

    # get routes from device
    my_swicth.sync_routes()
    count = my_swicth.routes.count
    static_routes = my_swicth.routes.static_list
    eigrp_routes = my_swicth.routes.eigrp_list

    print("Total Number of routes = %i" % count)
    print("Total Number of static routes = %i" % len(static_routes))
    print("Total Number of static routes = %i" % len(eigrp_routes))
    print_routes(my_swicth.routes.all)

    # add static route to device
    my_swicth.routes.add(network='10.10.1.1', netmask='255.255.255.0', nexthop_ip='1.1.1.4')
    is_ok, err_msg = my_swicth.commit()
    if is_ok:
        print("route added successfully ")

    # delete the route from device
    my_swicth.routes.delete(network='10.10.1.1', netmask='255.255.255.0', nexthop_ip='1.1.1.4')
    is_ok, err_msg = my_swicth.commit()
    if is_ok:
        print("route deleted successfully ")

    # you can add delete update multiple routes and call .commit() once to apply all commands at once


if __name__ == '__main__':
    main()

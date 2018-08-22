"""
Config component are the features in cisco devices like (routes,acl,vlans ... etc)
"""

class BaseConfig(object):
    """
    base object of single component like a Vlan , a route
    """
    def __init__(self, output):
        """
        set self the attributes we get from the device output dict,
        output example : {'id':'1', 'description':'vlan 1 description', 'interfaces':['ethernet1','ethernet2']}
        then we do
        self.id = 1
        self.description = 'vlan 1 description'
        self.interfaces = ['ethernet1','ethernet2']
        :param output:
        """
        for key, value in output.items():
            self.__setattr__(key, value)

    @property
    def deserialize(self):
        """
        deserialize the object to dict
        :return:
        """
        return vars(self)

    def __str__(self):
        return str(self.deserialize)


class BaseConfigs(object):
    """
    base object for a list of components like (vlans,interfaces)
    we need this object to group all vlans under one attribute in device manager ,
    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.sync_vlans()

    my_switch now will have vlans attributes which group all vlan objects ,
    BaseConfigs will has it's own methods which applied on all it's childern ,
    for example

    my_switch.vlans.count  --> give the count of all vlans
    my_switch.vlans.all --> return list of all vlan objects

    you can loop through vlans

    for vlan in my_Switch.vlans:
        print(vlan.id)

    """
    model = BaseConfig
    all = []

    @property
    def count(self):
        return len(self)

    def __init__(self, component_dicts):
        for i in component_dicts:
            self.all.append(self.model(i))

    def __len__(self):
        return len(self.all)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.all):
            raise StopIteration

        obj = self.all[self.i]
        self.i += 1
        return obj

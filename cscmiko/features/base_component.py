"""
Config component are the features in cisco devices like (routes,acl,vlans ... etc)
"""
from cscmiko.tools.config import render_command


def validate_cmd_inputs(kwargs):
    # validate add(),delete() and update() inputs are strings
    for kwarg in kwargs:
        assert isinstance(kwarg, str), f"config inputs should be string not {type(kwarg)}"


class Feature(object):
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


class FeatureSet(object):
    """
    base object for a list of components like (vlans|interfaces)
    we need this object to group all vlans under one attribute in device manager ,
    my_swicth = CatSwitch(host='4.71.144.98', username='admin', password='J3llyfish1')
    my_swicth.sync_vlans()

    my_switch now will have vlans(which is FeatureSet object) attribute which group all vlan objects ,
    FeatureSet will has it's own methods which applied on all it's children ,
    for example

    my_switch.vlans.count  --> give the count of all vlans
    my_switch.vlans.all --> return list of all vlan objects

    my_switch.vlans.add(id="1",name="aa")

    you can loop through vlans

    for vlan in my_Switch.vlans:
        print(vlan.id)

    """
    model = Feature
    conf_template = ""
    all = []
    cmds = []

    @property
    def count(self):
        return len(self)

    def __init__(self, component_dicts):
        for i in component_dicts:
            self.all.append(self.model(i))

    def add(self, **kwargs):
        """
        add config to device , exampe my_switch.vlans.add(id="1",name="vlan1")
        :param kwargs: config parameters
        :return:
        """
        validate_cmd_inputs(kwargs)
        kwargs.update({"action": "add"})
        cmds = render_command(self.conf_template, kwargs)
        self.cmds += cmds

    def delete(self, **kwargs):
        """
        delete component , example my_switch.vlans.delete(id="1")
        :param kwargs:
        :return:
        """
        validate_cmd_inputs(kwargs)
        kwargs.update({"action": "delete"})
        cmds = render_command(self.conf_template, kwargs)
        self.cmds += cmds

    def update(self, **kwargs):
        validate_cmd_inputs(kwargs)
        kwargs.update({"action": "update"})
        cmds = render_command(self.conf_template, kwargs)
        self.cmds += cmds

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

"""
Config component are the features in cisco devices like (routes,acl,vlans ... etc)
"""
from cscmiko.tools.config import render_command
from functools import wraps


def validate_cmd_inputs(kwargs):
    # validate add(),delete() and update() inputs are strings
    for kwarg in kwargs:
        assert isinstance(kwarg, str), f"config inputs should be string not {type(kwarg)}"


def _check_configurable(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].conf_template:
            raise TypeError(f"feature {type(args[0])._feature_name} is not configurable")

        return func(*args, **kwargs)

    return wrapper


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
            if not value:
                value = None
            setattr(self,key, value)

    @property
    def deserialize(self):
        """
        deserialize the object to dict
        :return:
        """
        return vars(self)

    def __str__(self):
        return str(self.deserialize)

    def __getitem__(self, item):
        return getattr(self, item)

    def __eq__(self, other):
        if isinstance(other, dict):  # __equal__ should accept dict or Feature object
            return self.deserialize == other
        elif isinstance(other, Feature):
            return self.deserialize == other.deserialize
        return False


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
    _feature_name = ""

    cmds = []

    @property
    def count(self):
        return len(self)

    def __init__(self, component_dicts):
        self.all = []
        for i in component_dicts:
            self.all.append(self.model(i))

    @_check_configurable
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

    @_check_configurable
    def delete(self, **kwargs):
        """
        delete configuration feature , example my_switch.vlans.delete(id="1")
        :param kwargs:
        :return:
        """
        validate_cmd_inputs(kwargs)
        kwargs.update({"action": "delete"})
        cmds = render_command(self.conf_template, kwargs)
        self.cmds += cmds

    @_check_configurable
    def update(self, **kwargs):
        """update device configuration"""
        validate_cmd_inputs(kwargs)
        kwargs.update({"action": "update"})
        cmds = render_command(self.conf_template, kwargs)
        self.cmds += cmds

    def filter(self, **kwargs):
        results = self.all.copy()  # .all should be copied as we will be poping results while iterating through self.all

        for item in self.all:
            for key, value in kwargs.items():
                if not hasattr(self.all[0], key):
                    raise AttributeError(f"{self._feature_name} does not have attribute '{key}' ")
                if item[key].lower() != value.lower():
                    index = results.index(item)
                    results.pop(index)
                    break

        return results

    def __getitem__(self, item):
        return self.all[item]

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

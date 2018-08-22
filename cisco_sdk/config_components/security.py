from .base import BaseConfig, BaseConfigs
from collections import defaultdict


class Rule(BaseConfig):
    pass


class ACL:
    rules = []
    name = ''

    def __init__(self, name, rules):
        self.name = name
        for rule in rules:
            self.rules.append(Rule(rule))

    def is_extended(self):
        pass


class AccessLists(BaseConfigs):
    model = ACL

    def __init__(self, component_dicts):
        acl = defaultdict(list)
        for i in component_dicts:
            acl_name = i.pop('acl_name')
            acl[acl_name].append(i)
        for key, value in acl.items():
            self.all.append(ACL(name=key, rules=value))

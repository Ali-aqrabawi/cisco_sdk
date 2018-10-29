"""
this module has the security config components ,
it has more business logic on the components
"""

from .base_component import Feature, FeatureSet
from collections import defaultdict


class Rule(Feature):
    """
    single rule of an access-list
    """
    pass


class ACL:
    """
    an access-list which at least has one rule object
    """
    rules = []
    name = ''


    def __init__(self, name, rules):
        self.name = name
        for rule in rules:
            if not rule['line_num']:  # the root acl should not be counted as rule
                continue
            self.rules.append(Rule(rule))

    def is_extended(self):
        pass


class AccessLists(FeatureSet):
    """
    all device access-lists
    """
    _feature_name = 'access_lists'
    model = ACL
    conf_template = 'acl.j2'

    def __init__(self, component_dicts):
        acl = defaultdict(list)
        for i in component_dicts:
            acl_name = i.pop('name')
            acl[acl_name].append(i)
        for key, value in acl.items():
            self.all.append(ACL(name=key, rules=value))

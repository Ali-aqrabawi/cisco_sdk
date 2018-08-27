"""
this module has the system config components like cpu
it has more business logic on the components
"""

from .base_component import Feature, FeatureSet


class Cpu(Feature):
    @property
    def is_high(self):
        if int(self.cpu_5_sec) > 80:
            return True
        return False

    def is_higher_than(self, utilization):
        if int(self.cpu_5_sec) > utilization:
            return True
        return False


class Module(Feature):

    @property
    def is_active(self):
        if self.status == 'active':
            return True
        return False

    @property
    def is_ok(self):
        if self.status == 'ok':
            return True
        return False

    @property
    def is_down(self):
        if self.status == 'down':
            return True
        return False


class Modules(FeatureSet):
    """
    cisco "show module" for nexus and 6k
    """
    model = Module

    def get_module_by_model(self, model):
        for module in self.all:
            if model in module.model:
                return module

    @property
    def down_list(self):
        return [i for i in self.all if i.is_down]

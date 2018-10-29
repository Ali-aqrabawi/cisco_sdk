"""
this module has the system config components like cpu
it has more business logic on the components
"""

from .base_component import Feature, FeatureSet
from math import floor

class Inventory(Feature):
    def __init__(self, output):
        super().__init__(output)
        self.serial = self.serial[0]
        self.hardware = self.hardware[0]


class Cpu(Feature):
    def __init__(self, output):
        super().__init__(output)
        self.utilization = int(output['cpu_5_min'])

    @property
    def is_high(self):
        return self.utilization > 80

    def is_higher_than(self, utilization):
        return int(self.utilization) > utilization


class Memory(Feature):

    def __init__(self, output):
        super().__init__(output)
        proc_total = int(output['proccessor_total'])
        proc_used = int(output['proccessor_used'])
        io_total = int(output['io_total'])
        io_used = int(output['io_used'])
        self.process_usage = floor((proc_used / proc_total) * 100)
        self.io_usage = floor((io_used / io_total) * 100)

    @property
    def is_io_high(self):
        return self.io_usage > 80

    @property
    def is_proc_high(self):
        return self.process_usage > 80


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
    _feature_name = 'modules'
    model = Module

    def get_module_by_model(self, model):
        for module in self.all:
            if model in module.model:
                return module

    @property
    def down_list(self):
        return [i for i in self.all if i.is_down]

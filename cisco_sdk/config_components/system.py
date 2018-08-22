from .base import BaseConfig


class Cpu(BaseConfig):
    @property
    def is_high(self):
        if int(self.cpu_5_sec) > 80:
            return True
        return False

    def is_higher_than(self, utilization):
        if int(self.cpu_5_sec) > utilization:
            return True
        return False

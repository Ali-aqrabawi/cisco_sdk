class BaseConfig(object):
    def __init__(self, output):
        for key, value in output.items():
            self.__setattr__(key, value)

    @property
    def deserialize(self):
        return vars(self)

    def __str__(self):
        return str(self.deserialize)


class BaseConfigs(object):
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

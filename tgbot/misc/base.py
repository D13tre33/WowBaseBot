import json


class Base(dict):
    """Just base class"""

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    # def __getattribute__(self, item):
    #     # return self[name]
    #     return super.__getattribute__(self, item)
    #     return super().__getattribute__(self, item)
    #
    # def __getattr__(self, name):
    #     return self[name]

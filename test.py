import re
from typing import Dict, Any, TYPE_CHECKING
from types import SimpleNamespace
import operator
from numpy import double

text = "You can run this command again in 2 seconds The default cooldown is 5s, but patrons only need to wait 1s!"
text_lst = text.split(" ")
index = text_lst.index("in")
print(double(text_lst[index + 1]))
text = "In SUShi (853102946841919519) (#🤖｜dank-memer), your bank is being robbed! The bankrob is being led by BananaJuic3#6969 (@BananaJuic3). Oh no!"
#text = text.split("led by ")[1]
print(text)
#text = text.split("channels/")[1]
m = re.search(r'[\w]+#+\d{1,9}', text)
if m:
    found = m.group(0)
    print(found)
else:
    print("not found")


class Dict2Class(object):
    def __init__(self, my_dict: Dict[str, str]):
        super().__init__()
        for key, v in my_dict.items():
            self.__setattr__(key, v)
    
    def __setattr__(self, name: str, value: Any) -> None:
        super(Dict2Class, self).__setattr__(name, value)
        return

class My(object):
    def __init__(self) -> None:
        self.device = self  

class MyTest(object):
    def __init__(self, x):
        self.x = x

    @property
    def device(self):
        return self
        
if TYPE_CHECKING:
    AttrDict = Any
else:
    class AttrDict(dict):
        def __init__(self, *args, **kwargs) -> None:
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self


def dict_to_attrdict(some: Dict[str, Any]) -> AttrDict:
    return AttrDict(**some)


if __name__ == '__main__':

    my_dict = {"Name": "Geeks",
               "Rank": "1223",
               "Subject": "Python"}
    obj = Dict2Class(my_dict)
    
    bee = operator.itemgetter('Name')
    print(bee(my_dict))

    ob2 = SimpleNamespace(lmao=1, funny=2)
    ob2.__eq__(my_dict)

    print(ob2)
    print(ob2.lmao)

    obj3 = AttrDict()
    obj3.x = 10
    print(obj3.x)

    attr_dict = dict_to_attrdict(some=my_dict)
    print(attr_dict.Name)
    print(attr_dict.Name)

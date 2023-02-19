"""
Есть фрагмент кода:

class TEST():
    red = 'red'
    green = 'green'
    blue = 'blue'


for color in TEST:
    print(color)

Допишите его, чтобы он корректно отработал, блок for и поля класса
менять нельзя, нельзя добавлять методы этому классу
"""


class IterableTest(type):
    def __iter__(cls):
        attributes = []
        for attr_name in cls.__dict__.keys():
            if not attr_name.startswith('_'):
                attr_value = getattr(cls, attr_name)
                if not callable(attr_value):
                    attributes.append(attr_value)
        return iter(attributes)


class TEST(metaclass=IterableTest):
    red = 'red'
    green = 'green'
    blue = 'blue'


for color in TEST:
    print(color)

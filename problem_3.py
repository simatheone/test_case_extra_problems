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


class TestClass(metaclass=IterableTest):
    red = 'red1'
    blue = 'blue1'
    green = 'green1'
    _hidden_1 = 'hidden1'
    __hidden_2 = 'hidden2'

    def new_method_1(self):
        ...

    def _new_method_2(self):
        ...

    def __new_method_3(self):
        ...


def test_correct_iteration_over_class_attrs(TestClass):
    result = []
    for color in TestClass:
        result.append(color)
    assert result == ['red1', 'blue1', 'green1']
    return 'test_correct_iteration_over_class -> Correct'


print(test_correct_iteration_over_class_attrs(TestClass))

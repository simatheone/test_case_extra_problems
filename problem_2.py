"""
Есть строка, с любыми символами.
Строка может содержать также 4 вида скобок: <> [] {} ()
Встречаться они могут одновременно в любом порядке, могут отсутствовать.

Необходимо реализовать проверку правильности скобочной записи.

Критерии: для каждой открывающейся скобки должна быть закрывающаяся, а также
должна быть корректная вложенность скобок.

Если критерии выполняются - вернуть true.
Если нет - вернуть индекс первой некорректной скобки в строке.

Например, строка ффф(ччч[ссс)ккк]
В ней первая некорректная скобка ) - 12 позиция
Поскольку ожидалась либо любая открывающаяся скобка, либо ]

Если закрывающихся скобок вообще нет - вернуть позицию последней скобки.
"""


def parentheses_sequence(input_seq):
    stack = []
    open_parentheses_symbols = frozenset(
        ['<', '{', '[', '(',]
    )
    parentheses_dict = {
        '>': '<',
        '}': '{',
        ']': '[',
        ')': '(',
    }

    last_opened_parenthesis_idx = None
    for index, character in enumerate(input_seq):
        if character in open_parentheses_symbols:
            stack.append(character)
            last_opened_parenthesis_idx = index + 1

        if character in parentheses_dict:
            if not stack or stack.pop() != parentheses_dict[character]:
                return index + 1

    if stack:
        return last_opened_parenthesis_idx
    return True


def test_valid_parentheses_sequence():
    sequence_1 = '<123{sdfasdf[hjdns123](dnjdii)dlksjdf}sdfasdf>'
    sequence_2 = '123<ffff[sss(ssss{111(666)dsss}sdsd)sdsdsd]>555'
    assert parentheses_sequence(sequence_1) is True
    assert parentheses_sequence(sequence_2) is True
    return 'test_valid_parentheses_sequence -> Correct'


def test_invalid_parentheses_sequence():
    sequence_1 = 'ааа[ббввд123<123лы>ова}ывлаолыв>'
    sequence_2 = 'ааа[ббввд123<123лыова}ывла>олыв]sdas'
    sequence_3 = 'ффф(ччч[ссс)ккк]'
    assert parentheses_sequence(sequence_1) == 23
    assert parentheses_sequence(sequence_2) == 22
    assert parentheses_sequence(sequence_3) == 12
    return 'test_invalid_parentheses_sequence -> Correct'


def test_no_close_parentheses():
    sequence_1 = '<111{hhhhhтттт[fjfjjf(ffddffds[dd'
    sequence_2 = '<'
    sequence_3 = '<[({'
    assert parentheses_sequence(sequence_1) == 31
    assert parentheses_sequence(sequence_2) == 1
    assert parentheses_sequence(sequence_3) == 4
    return 'test_no_close_parentheses -> Correct'


def test_no_parentheses_is_true():
    sequence_1 = ''
    sequence_2 = 'gggghhhhhbbbbmmmm'
    assert parentheses_sequence(sequence_1) is True
    assert parentheses_sequence(sequence_2) is True
    return 'test_no_parentheses_is_true -> Correct'


def test_no_open_parentheses_return_index():
    sequence_1 = ']<>{}[]()'
    sequence_2 = 'g]ggghhhhhbbbbmmmm'
    assert parentheses_sequence(sequence_1) == 1
    assert parentheses_sequence(sequence_2) == 2
    return 'test_no_parentheses_is_true -> Correct'


tests = (
    test_valid_parentheses_sequence, test_invalid_parentheses_sequence,
    test_no_close_parentheses, test_no_parentheses_is_true,
    test_no_open_parentheses_return_index
)

if __name__ == '__main__':
    for test in tests:
        print(test())

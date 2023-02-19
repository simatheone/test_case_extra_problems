"""
Реализовать числа Фибоначчи с использованием хвостовой рекурсии.
"""


def fibo(n, a=0, b=1):
    if n == 0:
        return a
    if n == 1:
        return b
    return fibo(n - 1, b, b + a)


def test_recursion_fibo():
    assert fibo(3) == 2
    assert fibo(6) == 8
    assert fibo(8) == 21
    return 'test_recursion_fibo -> Correct'


print(test_recursion_fibo())

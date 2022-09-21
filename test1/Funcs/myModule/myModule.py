
def max(arr):
    m = arr[0]

    for n in arr:
        if n > m:
            m = n

    return m


def min(arr):
    m = arr[0]

    for n in arr:
        if n < m:
            m = n

    return m


def sum(arr):
    s = 0

    for n in arr:
        s += n

    return s


def myDiv(a, b):
    try:
        res = a / b
    except ZeroDivisionError:
        return '«бесконечность»'
    else:
        return res

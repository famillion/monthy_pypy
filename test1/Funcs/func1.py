from random import randint as rand


def isEven(dig):
    if dig % 2 == 0:
        return True
    else:
        return False


def maxNum(arr: list):
    max = arr[0]

    for n in arr:
        if n > max:
            max = n

    return max


def midNum(*nums):
    sum = 0

    for n in nums:
        sum += n

    return sum / len(nums)


print('--' * 20)
print(isEven(33))
print(isEven(12))
print('--' * 20)

print('--' * 20)
arr = [rand(1, 100) for i in range(10)]
print(arr)
print(maxNum(arr))
print('--' * 20)

print('--' * 20)
print(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(midNum(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
print('--' * 20)
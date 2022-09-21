import myModule
from random import randint as rand


arr = [rand(0, 44) for i in range(10)]

print('--' * 20)
print(arr)
print('--' * 20)

print('--' * 20)
print('max =', myModule.max(arr))
print('--' * 20)

print('--' * 20)
print('min =', myModule.min(arr))
print('--' * 20)

print('--' * 20)
print('sum', myModule.sum(arr))
print('--' * 20)

print('--' * 20)
a = int(input('enter a:'))
b = int(input('enter b:'))
print('res', myModule.myDiv(a, b))
print('--' * 20)
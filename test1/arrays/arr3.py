from random import randint as rand

num = int(input('ввести количество элементов для списка: '))

arr = [rand(0, 14) for i in range(num)]

print('-' * 20)
print(arr)
print('-' * 20)

ind = 0
while ind < len(arr):
    print(arr[ind])
    ind += 1

arr2 = set(arr)

print('-' * 20)
print(arr2)
print('-' * 20)

for j in arr2:
    print(j)

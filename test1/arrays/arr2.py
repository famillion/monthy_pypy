from random import randint as rand

arr = [rand(0, 20) for i in range(5)]

print('Massiv ---', arr)
print('-' * 20)

sum = 0

for n in arr:
    sum += n

print('Summa chisel massiva ---', sum)
print('-' * 20)

print('Srednee ---', sum/len(arr))



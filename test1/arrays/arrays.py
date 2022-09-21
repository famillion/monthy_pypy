arrStr = ['Попросите', 'пользователя', 'ввести', 'индекс', 'того', 'элемента', 'значение',
          'которого', 'он', 'хочет', 'посмотреть']


for i in arrStr:
    print(arrStr.index(i), '--', i)

print('*' * 20)

while True:
    ind = int(input('ввести индекс того элемента (-1 quit):'))

    if ind == -1:
        break
    if ind > (len(arrStr) - 1) or ind < -1:
        print('index incorrect')
        continue
    else:
        print(arrStr[ind])

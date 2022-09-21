import random

randNumOt = int(input ( 'число от: ' ))
randNumDo = int(input ( 'число до: ' ))

rand = random.randint ( randNumOt, randNumDo )

scores = 100

num = (randNumDo + 1)

while num != rand and scores > 0:
    num = int(input("Enter number: "))

    if num > rand:
        print('Mimo! <')
    elif num < rand:
        print('Mimo! >')
    elif num == rand:
        print('Bingo!')
        break

    scores -= 10

if scores <= 0:
    print('Congrats! You LOSE! Your scores -', scores, '==== NUM ===', rand)
else:
    print('Congrats! You Win! Your scores -', scores, '==== NUM ===', rand)

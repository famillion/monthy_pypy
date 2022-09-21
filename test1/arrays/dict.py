myDict = dict(Name='none', Age=-1)

print('-' * 20)
print(myDict)
print('-' * 20)

myDict = {'Name': input('ввести своё имя'), 'Age': input('ввести свой возраст')}

print('-' * 20)
print(myDict)
print('-' * 20)

for key in myDict:
    print(key, '-', myDict[key])

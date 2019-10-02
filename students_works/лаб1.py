
def func(char,height,width) :
    line = char * width
    rectangle = ((line + '\n')* height)
    return rectangle
print("Костюк Владислава \nКМ-93 \nЛабораторна №1\nВаріант №10\nЗавдання №1\nОбчислення в математичних задачах\nВиведення прямокутника який складається з букви А\n")
print(func('A',5,8))
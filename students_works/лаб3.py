print("Костюк Владислава \nКМ-93 \nЛабораторна №1\nВаріант №10\nЗавдання №2")
def second_task():
    print('Введіть перше число')
    while 1:
        try:
            a = float(input())
            break
        except ValueError:
            print("Ви помилились. Спробуйте знову.")
    print('Введіть друге число ')
    while 1:
        try:
            b = float(input())
            break
        except ValueError:
            print("Ви помилились. Спробуйте знову.")
    print('Введіть третє число')
    while 1:
        try:
            c = float(input())
            break
        except ValueError:
            print("Ви помилились. Спробуйте знову.")
    print('Введіть четверте число')
    while 1:
        try:
            k = float(input())
            break
        except ValueError:
            print("Ви помилились. Спробуйте знову.")
    if a % k == 0:
        print('Четверте число є дільником першого числа')
    elif b % k == 0:
        print('Четверте число є дільником другого числа')
    elif c % k == 0:
        print('Четверте число є дільником третього числа')
    else:
        print('Четверте число не є дільником жодного з чисел')

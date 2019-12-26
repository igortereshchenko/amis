import math

from dao import db
from dao.orm.entities import *


def calcY(X, Input):
    ExpSum = 0.0
    for x in X:
        AbsSum = 0.0
        for i in range(len(Input)):
            AbsSum += (x[i] - Input[i]) ** 2
        ExpSum += math.exp(-AbsSum / 0.09)
    return ExpSum / len(X)


def calcExample(x, map, classes):
    y = []
    for c in classes:
        y.append(calcY(c, x))
    # print(y)
    max_index = y.index(max(y))
    for key, value in map.items():
        if value == max_index:
            # print(str(x) + " is class " + key)
            return key


def create_model():
    classes = []
    classes.append([[3, 24], [5, 48], [3, 20]])
    classes.append([[1, 24], [2, 48]])
    res = {}
    map = {'hard': 0, 'light': 1, 'minor': 2}
    connect = db.PostgresDb()
    disciplines = connect.sqlalchemy_session.query(Discipline).all()
    for d in disciplines:
        tasks = connect.sqlalchemy_session.query(Task).filter(Task.discipline_name == d.name).all()
        sum = 0.0
        for t in tasks:
            sum += t.deadline.hour + t.deadline.minute / 60.0
        res[d.name] = calcExample([len(tasks), sum], map, classes)
    return res

if __name__ == '__main__':
    create_model()

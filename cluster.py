import os
import pickle
import numpy as np
from sklearn.cluster import KMeans

from dao import db
from dao.orm.entities import *
from datetime import datetime
from datetime import time
def create_model(source_path=""):
    connect = db.PostgresDb()
    disciplines = connect.sqlalchemy_session.query(Discipline).all()
    task = []
    for d in disciplines:
        tasks = connect.sqlalchemy_session.query(Task).filter(Task.discipline_name == d.name).all()
        sum = 0.0
        for t in tasks:
            sum+=t.deadline.hour+t.deadline.minute/60.0
        task.append([len(tasks),sum])

    x = np.array([[t[0],t[1]] for t in task])

    k_means = KMeans(n_clusters=2, random_state=0).fit(x)
    pickle.dump(k_means, open(source_path + "save_cluster.pkl", "wb"))
    np.savetxt(source_path + 'x_csv.csv', x, delimiter=',')
    return k_means, x


def get_cluster_val(student_name=0, source_path=""):
    if not os.path.exists(source_path + "save_cluster.pkl"):
        k_means, marks_all = create_model()
    else:
        marks_all = np.genfromtxt(source_path + "x_csv.csv", delimiter=',')
        k_means = pickle.load(open(source_path + "save_cluster.pkl", "rb"))

    c = k_means.cluster_centers_
    #  good == 1/0, deside what number is good and what is bad
    good_label = k_means.predict([c[-1]])[0]

    # todo add bad and good labels
    c_x = [point[0] for point in c]
    c_y = [point[1] for point in c]

    labels = np.array(k_means.labels_, dtype=bool)
    if good_label:
        marks_good_cluster = marks_all[labels]
        marks_bad_cluster = marks_all[~labels]
    else:
        marks_good_cluster = marks_all[~labels]
        marks_bad_cluster = marks_all[labels]

    if student_name > "":
        connect = db.PostgresDb()
        disciplines = connect.sqlalchemy_session.query(Discipline).all()
        task = []
        for d in disciplines:
            tasks = connect.sqlalchemy_session.query(Task).filter(Task.discipline_name == d.name).all()
            sum = 0.0
            for t in tasks:
                sum += t.deadline.hour + t.deadline.minute / 60.0
            task.append([len(tasks), sum])

        x = np.array([[t[0], t[1]] for t in task])

        labels_student = k_means.predict(x)
        return c_x, c_y, marks_good_cluster, marks_bad_cluster, x, "hard" if max(
            labels_student) == good_label else "light"

    return c_x, c_y, labels, marks_good_cluster, marks_bad_cluster


if __name__ == '__main__':
    create_model()

import os
import pickle
import numpy as np
from sklearn.neural_network import MLPRegressor

from source.dao import db
from source.dao.orm.entities import *


def create_model(source_path=""):
    connect = db.PostgresDb()
    marks = connect.sqlalchemy_session.query(StudentRecordBook).filter(StudentRecordBook.final_mark != 0).all()
    x = np.array([[record.semester_mark, record.discipline_id_fk, record.professor_id_fk] for record in marks])
    y = np.array([[record.final_mark] for record in marks])

    multi_layer_perceptron = MLPRegressor(hidden_layer_sizes=10, solver="lbfgs").fit(x, y)
    pickle.dump(multi_layer_perceptron, open(source_path + "save_regression.pkl", "wb"))
    print(multi_layer_perceptron.loss_)
    return multi_layer_perceptron


def get_regression_val(source_path="source/analysis/", semester_val=30, discipline_id=1, professor_id=1):
    connect = db.PostgresDb()
    prof = connect.sqlalchemy_session.query(Professor).filter(Professor.professor_id == professor_id).all()
    disc = connect.sqlalchemy_session.query(Professor).filter(Discipline.discipline_id == discipline_id).all()
    if not prof or not disc:
        return 0

    if not os.path.exists(source_path + "save_regression.pkl"):
        multi_layer_perceptron = create_model(source_path='source/analysis/')
    else:
        multi_layer_perceptron = pickle.load(open(source_path + "save_regression.pkl", "rb"))

    return np.round(multi_layer_perceptron.predict([[semester_val, discipline_id, professor_id]])[0])


if __name__ == '__main__':
    create_model()

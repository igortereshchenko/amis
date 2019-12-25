import os
from random import random, randrange

from app import app
from neural_network_model.db.connection import conn
from neural_network_model.load_dataset import parse_data_from_file

# populate disciplines


def populate_from_dataset():

    file_path = os.path.join(app.root_path, 'neural_network_model', 'data/test_data.json')

    data = parse_data_from_file(file_path)

    disciplines = list(set([item['discipline'] for item in data]))
    cursor = conn.cursor()
    for i, discipline in enumerate(disciplines):
        try:
            cursor.execute(
                "INSERT INTO orm_discipline (id, name) values ({}, '{}');".format(
                    i+1, str(discipline)
                )
            )
            conn.commit()
        except Exception as e:
            print(e.args)

    # populate questions

    i = 0
    for item in data:
        i += 1
        if i > 200:
            try:
                cursor.execute(
                    "INSERT INTO orm_question (question_text, discipline_id, test_id) values ('{}', {}, {});".format(
                        item.get('question').replace("'", ''),
                        int(disciplines.index(item.get('discipline').replace('\n', ''))) + 1,
                        randrange(1, 4, 1)
                    )
                )
                conn.commit()
            except Exception as e:
                print(e.args)
        if i > 600:
            break

populate_from_dataset()
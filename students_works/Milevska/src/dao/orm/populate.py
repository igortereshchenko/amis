from dao.orm.model import *
from dao.db import PostgresDB
# from neural_network_model.db.populate import populate_from_dataset

db = PostgresDB()

Base.metadata.create_all(db.sqlalchemy_engine)


session = db.sqlalchemy_session

session.query(ormAnswerVariant).delete()
session.query(ormQuestion).delete()
session.query(ormTest).delete()
session.query(ormUser).delete()

test_1_v_1 = ormTest(
    test_name='First test',
)

test_1_v_2 = ormTest(
    test_name='Second test',
)

test_1_v_3 = ormTest(
    test_name='Third test',
)

test_2_v_1 = ormTest(
    test_name='Fourth test',
)

session.add_all([
    test_1_v_1, test_1_v_2, test_1_v_3, test_2_v_1,
])
session.commit()

test_1_v_1_question_1 = ormQuestion(
    question_text='How are u?',
    test_id=test_1_v_1.test_id,
)

test_1_v_1_question_2 = ormQuestion(
    question_text='What is your name?',
    test_id=test_1_v_1.test_id,
)

test_1_v_1_question_3 = ormQuestion(
    question_text='How old are you?',
    test_id=test_1_v_1.test_id,
)

test_1_v_2_question_1 = ormQuestion(
    question_text='What is your favourite color?',
    test_id=test_1_v_1.test_id,
)

session.add_all([
    test_1_v_1_question_1, test_1_v_1_question_2, test_1_v_1_question_3, test_1_v_2_question_1,
])
session.commit()

test_1_v_1_question_1_variant_1 = ormAnswerVariant(
    answer_variant_text='Fine',
    question_id=test_1_v_1_question_1.question_id
)

test_1_v_1_question_1_variant_2 = ormAnswerVariant(
    answer_variant_text='Bad',
    question_id=test_1_v_1_question_1.question_id,
    answer_check=True
)

test_1_v_1_question_1_variant_3 = ormAnswerVariant(
    answer_variant_text='so-so',
    question_id=test_1_v_1_question_1.question_id
)

test_1_v_1_question_2_variant_1 = ormAnswerVariant(
    answer_variant_text='Hanna',
    question_id=test_1_v_1_question_2.question_id
)

test_1_v_1_question_2_variant_2 = ormAnswerVariant(
    answer_variant_text='Olya',
    question_id=test_1_v_1_question_2.question_id,
    answer_check=True
)

session.add_all([
    test_1_v_1_question_1_variant_1, test_1_v_1_question_1_variant_2, test_1_v_1_question_1_variant_3,
    test_1_v_1_question_2_variant_1, test_1_v_1_question_2_variant_2])

session.commit()

user_1 = ormUser(
    email='admin@mail.com',
    password='qwerty123',
    role='ADMIN',
    first_name='First',
    last_name='Admin'
)

user_2 = ormUser(
    email='test@mail.com',
    password='qwerty123',
    role='STANDARD',
    first_name='First',
    last_name='Standard'
)
session.add_all([user_1, user_2])
session.commit()

# populate_from_dataset()

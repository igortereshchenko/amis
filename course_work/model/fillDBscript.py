from model.model import db, QuestionsTable, QuestionnaireTable, AnswerTable, UniversityUsersTable


def fill_users_script():
    admin = UniversityUsersTable(UserFullName="Admin Admin",
                                 User_email="admin@kpi.ua",
                                 User_password="Passw0rd!",
                                 User_faculty="Admin role"
                                 )
    student_1 = UniversityUsersTable(UserFullName="Bob Bobov",
                                     User_email="bob@kpi.ua",
                                     User_password="Passw0rd!",
                                     User_faculty="TEF"
                                     )
    student_2 = UniversityUsersTable(UserFullName="Boba Bobenko",
                                     User_email="boba@kpi.ua",
                                     User_password="Passw0rd!",
                                     User_faculty="XTF"
                                     )
    student_3 = UniversityUsersTable(UserFullName="Bobik Bobenchuk",
                                     User_email="bobik@kpi.ua",
                                     User_password="Passw0rd!",
                                     User_faculty="FPM"
                                     )

    db.session.add_all([admin, student_1, student_2, student_3])


def fill_questions_script():
    question_edu_1 = QuestionsTable(
        Questions="What foreign language do you prefer?",
        Type_question="Educational"
    )

    question_edu_2 = QuestionsTable(
        Questions="What additional lesson do you need?",
        Type_question="Educational"
    )

    question_ent_1 = QuestionsTable(
        Questions="Where do you want to spend time more?",
        Type_question="Entertainment"
    )

    question_ent_2 = QuestionsTable(
        Questions="What event do you want to see?",
        Type_question="Entertainment"
    )

    question_imp_1 = QuestionsTable(
        Questions="What classroom we need to repair?",
        Type_question="Improvement"
    )

    question_imp_2 = QuestionsTable(
        Questions="What building does need to be rebuilt",
        Type_question="Improvement"
    )

    question_mng_1 = QuestionsTable(
        Questions="What subject do you want to improve?",
        Type_question="Management"
    )

    question_mng_2 = QuestionsTable(
        Questions="What should be improved at all?",
        Type_question="Management"
    )

    db.session.add_all(
        [question_edu_1, question_edu_2, question_ent_1, question_ent_2, question_imp_1, question_imp_2, question_mng_1,
         question_mng_2])


def fill_questionnaires_script():
    questionnaire_1 = QuestionnaireTable(
        Questionnaire_id=1,
        User_faculty="TEF",
        QuestionIdFk=1
    )

    questionnaire_2 = QuestionnaireTable(
        Questionnaire_id=1,
        User_faculty="TEF",
        QuestionIdFk=2
    )

    questionnaire_3 = QuestionnaireTable(
        Questionnaire_id=2,
        User_faculty="TEF",
        QuestionIdFk=2
    )

    questionnaire_4 = QuestionnaireTable(
        Questionnaire_id=2,
        User_faculty="TEF",
        QuestionIdFk=3
    )

    db.session.add_all([questionnaire_1, questionnaire_2, questionnaire_3, questionnaire_4])


def fill_answers_script():
    answ_1 = AnswerTable(
        Answer_for_question="Italian",
        User_faculty="TEF",
        StudentIdFk="bob@kpi.ua",
        QuestionIdFk=1
    )

    answ_2 = AnswerTable(
        Answer_for_question="Physics",
        User_faculty="TEF",
        StudentIdFk="bob@kpi.ua",
        QuestionIdFk=2
    )

    db.session.add_all([answ_1, answ_2])

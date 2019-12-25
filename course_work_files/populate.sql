INSERT INTO users_table (user_fullname, user_email, user_password, user_faculty)
VALUES ('Admin Admin', 'admin@kpi.ua', 'Passw0rd!', 'Admin role');

INSERT INTO users_table (user_fullname, user_email, user_password, user_faculty)
VALUES ('Bob Bobov', 'bob@kpi.ua', 'Passw0rd!', 'TEF');

INSERT INTO users_table (user_fullname, user_email, user_password, user_faculty)
VALUES ('Boba Bobenko', 'boba@kpi.ua', 'Passw0rd!', 'XTF');

INSERT INTO questions_table (question_id, questions, type_question)
VALUES (1, 'What foreign language do you prefer?', 'Educational');

INSERT INTO questions_table (question_id, questions)
VALUES (2, 'What additional lesson do you need?', 'Educational');

INSERT INTO questions_table (question_id, questions)
VALUES (3, 'What classroom we need to repair?', 'Improvement');

INSERT INTO questions_table (question_id, questions)
VALUES (4, 'Where do you want to spend time more?', 'Entertainment');

INSERT INTO questionnaire_table (questionnaire_id, user_faculty, question_id_fk)
VALUES (1, 'educational', 1);

INSERT INTO questionnaire_table (questionnaire_id, user_faculty, question_id_fk)
VALUES (1, 'educational', 2);

INSERT INTO questionnaire_table (questionnaire_id, user_faculty, question_id_fk)
VALUES (2, 'improvement', 3);

INSERT INTO answer_table (answer_id, answer_for_question, user_faculty, student_id_fk, question_id_fk)
VALUES (1, 'Italian', 'TEF', 'bob@kpi.ua', 1);

INSERT INTO answer_table (answer_id, answer_for_question, user_faculty, student_id_fk, question_id_fk)
VALUES (2, 'Physics', 'TEF', 'bob@kpi.ua', 2);

INSERT INTO answer_table (answer_id, answer_for_question, user_faculty, student_id_fk, question_id_fk)
VALUES (3, '92-15', 'XTF', 'boba@kpi.ua', 3);

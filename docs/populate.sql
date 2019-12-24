INSERT INTO groups (name) VALUES ('KM-61');
INSERT INTO groups (name) VALUES ('KM-62');
INSERT INTO groups (name) VALUES ('KM-63');

SELECT * FROM groups;


INSERT INTO users (full_name, type, user_id, date_registered, group_id) VALUES ('Test User1', 'student', 1, '2019-11-10', 1);
INSERT INTO users (full_name, type, user_id, date_registered, group_id) VALUES ('Test User2', 'student', 2, '2019-11-11', 2);
INSERT INTO users (full_name, type, user_id, date_registered, group_id) VALUES ('Test User3', 'teacher', 3, '2019-11-12', 3);

SELECT * FROM users;


INSERT INTO lecture_packs (pack_name, description) VALUES ('pack1', 'desc1');
INSERT INTO lecture_packs (pack_name, description) VALUES ('pack2', 'desc2');
INSERT INTO lecture_packs (pack_name, description) VALUES ('pack3', 'desc3');

SELECT * FROM lecture_packs;

INSERT INTO lectures (text, version, created, modified, pack_name, lecture_id)  VALUES ('some text', 1, '2019-11-10', '2019-11-10', 'pack1', 1);
INSERT INTO lectures (text, version, created, modified, pack_name, lecture_id, prev_lecture_id)  VALUES ('some text2', 2, '2019-11-10', '2019-11-11', 'pack1', 2, 1);
INSERT INTO lectures (text, version, created, modified, pack_name, lecture_id)  VALUES ('some text3', 3, '2019-11-12', '2019-11-12', 'pack2', 3);

SELECT * FROM lectures;


INSERT INTO lecture_comment (text, datetime, likes, lecture_id, user_id) VALUES ('text1', '2019-11-10', 1, 1, 1);
INSERT INTO lecture_comment (text, datetime, likes, lecture_id, user_id) VALUES ('text2', '2019-11-11', 2, 2, 2);
INSERT INTO lecture_comment (text, datetime, likes, lecture_id, user_id) VALUES ('text3', '2019-11-12', 3, 3, 3);

SELECT * FROM lecture_comment;


INSERT INTO lecture_activity (view_count, like_count, comment_count, student_id, lecture_id, lecture_activity_id, grade) VALUES (1, 1, 1, 1, 1, 1, 60);
INSERT INTO lecture_activity (view_count, like_count, comment_count, student_id, lecture_id, lecture_activity_id, grade) VALUES (2, 2, 2, 2, 2, 2, 75);
INSERT INTO lecture_activity (view_count, like_count, comment_count, student_id, lecture_id, lecture_activity_id, grade) VALUES (3, 3, 3, 3, 3, 3, 95);

SELECT * FROM lecture_activity;


INSERT INTO subjects (name, teacher_id, lecture_id) VALUES ('calculus', 1, 1);
INSERT INTO subjects (name, teacher_id, lecture_id) VALUES ('diff equations', 2, 2);
INSERT INTO subjects (name, teacher_id, lecture_id) VALUES ('dbis', 3, 3);

SELECT * FROM subjects;


INSERT INTO group_subjects (group_id, subject_name) VALUES (1, 'calculus');
INSERT INTO group_subjects (group_id, subject_name) VALUES (2, 'diff equations');
INSERT INTO group_subjects (group_id, subject_name) VALUES (3, 'dbis');

SELECT * FROM group_subjects;


INSERT INTO teacher_subjects (user_id, subject_name) VALUES (1, 'calculus');
INSERT INTO teacher_subjects (user_id, subject_name) VALUES (2, 'diff equations');
INSERT INTO teacher_subjects (user_id, subject_name) VALUES (3, 'dbis');


SELECT * FROM teacher_subjects;



insert into "Admin"(
                    login,
                    password)
values ('admin', 'admin');

-----------------------------------------------------------------------------------------------------------------------

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('kpi', 'fpm', 'km-61', 'eugene', 'patrushev', 'eugene', 'eugene');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('kpi', 'fpm', 'km-61', 'vova', 'pasko', 'vova', 'vova');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('kpi', 'fpm', 'km-61', 'nikita', 'mozgovoy', 'nikita', 'nikita');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('kpi', 'fpm', 'km-62', 'yarik', 'neznau', 'yarik', 'yarik');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('nau', 'fpp', 'ff-11', 'valera', 'valera', 'valera', 'valera');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('nau', 'fpp', 'ff-12', 'vova', 'vova', 'vova1', 'vova');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('sheva', 'pm', 'pm-61', 'mozgovoy', 'valera', '111', '111');

insert into "Student"(
                    student_university,
                    student_faculty,
                    student_group,
                    name,
                    surname,
                    login,
                    password)
values ('sheva', 'pm', 'pm-62', 'neznau', 'nikita', '222', '222');

-----------------------------------------------------------------------------------------------------------------------

insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('kpi', 'fpm', 'Volodimir', 'Malrchikov', 'professor');


insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('kpi', 'fpm', 'Tatiana', 'Ladogubets', 'professor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('kpi', 'fpm', 'Katia', 'Adamuk', 'doctor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('kpi', 'iasa', 'Denis', 'Lvovich', 'doctor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('nau', 'fpp', 'Maria', 'Adamuk', 'proffessor');

insert into "Professor"(
                    professor_university,
                    professor_department,
                    name,
                    surname,
                    professor_degree)
values ('sheva', 'pm', 'Victor', 'Nazarovich', 'doctor');

----------------------------------------------------------------------------------------------------------------------

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('kpi', 'fpm', 'Mat Analise', TRUE, 130);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('kpi', 'fpm', 'DB_2', TRUE, 120);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('kpi', 'fpm', 'English', FALSE, 90);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('kpi', 'fpm', 'Mat Stat', FALSE, 60);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('nau', 'fpp', 'programming', FALSE, 90);

insert into "Discipline"(discipline_university,
                       discipline_faculty,
                       discipline_name,
                       discipline_exam,
                       discipline_hours_for_semester)
values ('sheva', 'pm', 'Mat Stat', FALSE, 60);
----------------------------------------------------------------------------------------------------------------------

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 2, 2, 45, 85, '2019-12-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 3, 3, 50, 80, '2019-12-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                            exam_passed)
values (2, 4, 1, 45, '2019-12-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (2, 2, 2, 30, 60, '2019-12-18');


insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 1, 2, 50, 75, '2020-06-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (1, 4, 3, 40, 80, '2020-06-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                            exam_passed)
values (2, 3, 1, 45, '2020-06-15');

insert into "StudentRecordBook"(student_id_fk,
                              discipline_id_fk,
                              professor_id_fk,
                              semester_mark,
                              final_mark,
                              exam_passed)
values (2, 1, 2, 30, 60, '2020-06-18');
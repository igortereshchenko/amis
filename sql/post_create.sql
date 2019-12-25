CREATE TABLE "Student" (
    student_id int,
    student_university VARCHAR(255) NOT NULL,
    student_faculty VARCHAR(255) NOT NULL,
    student_group VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    student_date_enrollment DATE NOT NULL DEFAULT CURRENT_DATE,
    student_date_expelled DATE
);

ALTER TABLE "Student" ADD PRIMARY KEY (student_id);

ALTER TABLE "Student"
ADD CONSTRAINT unique_student_combination UNIQUE (student_university,
                                                  student_faculty,
                                                  student_group,
                                                  name,
                                                  surname);

ALTER TABLE "Student"
ADD CONSTRAINT unique_login UNIQUE (login);

CREATE SEQUENCE student_id_sequence START 1;

---------------------------------------------------------------------------------------------------------

CREATE TABLE "Admin" (
    id int,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

ALTER TABLE "Admin" ADD PRIMARY KEY (id);

CREATE SEQUENCE admin_id_sequence START 1;

---------------------------------------------------------------------------------------------------------

CREATE TABLE "Professor" (
    professor_id int,
    professor_university VARCHAR(255) NOT NULL,
    professor_department VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    professor_degree VARCHAR(255),
    professor_date_enrollment DATE NOT NULL DEFAULT CURRENT_DATE,
    professor_date_expelled DATE
);

ALTER TABLE "Professor" ADD PRIMARY KEY (professor_id);

ALTER TABLE "Professor"
ADD CONSTRAINT unique_professor_combination UNIQUE (professor_university,
                                                  professor_department,
                                                  name,
                                                  surname);

CREATE SEQUENCE professor_id_sequence START 1;

---------------------------------------------------------------------------------------------------------


CREATE TABLE "Discipline" (
    discipline_id int,
    discipline_university VARCHAR(255),
    discipline_faculty VARCHAR(255),
    discipline_name VARCHAR(255),
    discipline_exam BOOLEAN NOT NULL,
    discipline_hours_for_semester INT);

ALTER TABLE "Discipline" ADD PRIMARY KEY (discipline_id);

ALTER TABLE "Discipline"
ADD CONSTRAINT unique_discipline_combination UNIQUE (discipline_university,
                                                  discipline_faculty,
                                                  discipline_name);

CREATE SEQUENCE discipline_id_sequence START 1;

---------------------------------------------------------------------------------------------------------


CREATE TABLE "StudentRecordBook" (
    student_id_fk int,
    discipline_id_fk int,
    professor_id_fk int,

    semester_mark INT DEFAULT 0,
    final_mark INT DEFAULT 0,
    exam_passed  DATE
);

ALTER TABLE "StudentRecordBook" ADD PRIMARY KEY (student_id_fk, discipline_id_fk);

ALTER TABLE "StudentRecordBook"
ADD CONSTRAINT FOREIGN_KEY_StudentRecordBook_Student FOREIGN KEY (student_id_fk) REFERENCES "Student" (student_id);

ALTER TABLE "StudentRecordBook"
ADD CONSTRAINT FOREIGN_KEY_StudentRecordBook_Discipline FOREIGN KEY (discipline_id_fk) REFERENCES "Discipline" (discipline_id);

ALTER TABLE "StudentRecordBook"
ADD CONSTRAINT FOREIGN_KEY_StudentRecordBook_Professor FOREIGN KEY (professor_id_fk) REFERENCES "Professor" (professor_id);
---------------------------------------------------------------------------------------------------------


CREATE OR REPLACE FUNCTION check_fun() RETURNS trigger AS $$
        DECLARE
            uni VARCHAR(255);
            faculty VARCHAR(255);
            uni_discipline VARCHAR(255);
            faculty_discipline VARCHAR(255);
        BEGIN
            select student_university, student_faculty into uni, faculty from "Student"
            where student_id=NEW.student_id_fk;

            select discipline_university, discipline_faculty into uni_discipline, faculty_discipline from "Discipline"
            where discipline_id=NEW.discipline_id_fk;

            if uni = uni_discipline and faculty_discipline = faculty then
                select professor_university into uni from "Professor"
                where professor_id = NEW.professor_id_fk;
                if uni = uni_discipline then
                    return NEW;
                else
                    RAISE EXCEPTION 'professor from another university';
                end if;
            else
                RAISE EXCEPTION 'student and discipline from another uni or faculty';
            end if;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER check_insert_record_book
    BEFORE insert ON "StudentRecordBook"
    FOR EACH ROW
    EXECUTE PROCEDURE check_fun();

-------- student incr

CREATE OR REPLACE FUNCTION incr_student() RETURNS trigger AS $$
        BEGIN
            NEW.student_id = nextval('student_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER student_increment
    BEFORE insert ON "Student"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_student();

-------- professor incr

CREATE OR REPLACE FUNCTION incr_professor() RETURNS trigger AS $$
        BEGIN
            NEW.professor_id = nextval('professor_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;


CREATE TRIGGER professor_increment
    BEFORE insert ON "Professor"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_professor();

-------- discipline incr

CREATE OR REPLACE FUNCTION incr_discipline() RETURNS trigger AS $$
        BEGIN
            NEW.discipline_id = nextval('discipline_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER discipline_increment
    BEFORE insert ON "Discipline"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_discipline();

-------- admin incr

CREATE OR REPLACE FUNCTION incr_admin() RETURNS trigger AS $$
        BEGIN
            NEW.id = nextval('admin_id_sequence');
            return NEW;
        END;

$$  LANGUAGE plpgsql;

CREATE TRIGGER admin_increment
    BEFORE insert ON "Admin"
    FOR EACH ROW
    EXECUTE PROCEDURE incr_admin();

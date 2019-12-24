CREATE TABLE IF NOT EXISTS groups (
 group_id serial primary key,
 name varchar(6)
);

CREATE TABLE IF NOT EXISTS users (
 full_name varchar (250),
 type varchar (20),
 date_registered date,

 user_id SERIAL PRIMARY KEY,
 group_id integer,

 FOREIGN KEY (group_id) REFERENCES groups(group_id)
);

CREATE TABLE IF NOT EXISTS lecture_packs (
    pack_name varchar(150),
    description varchar(150),

    PRIMARY KEY (pack_name)
);

CREATE TABLE IF NOT EXISTS lectures (
    text text,
    version integer,
    created timestamp,
    modified timestamp,
    pack_name varchar(150),
    lecture_id SERIAL,
    prev_lecture_id integer null,

    PRIMARY KEY (lecture_id),
    FOREIGN KEY (prev_lecture_id) REFERENCES lectures(lecture_id),
    FOREIGN KEY (pack_name) REFERENCES lecture_packs(pack_name)
);

CREATE TABLE IF NOT EXISTS lecture_comment (
    text text,
    datetime timestamp,
    likes int,
    lecture_id int,
    user_id int,

    PRIMARY KEY (lecture_id, user_id, datetime),
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS lecture_activity (
    view_count int,
    like_count int,
    comment_count int,
    grade int,
    student_id int,
    lecture_id int,
    lecture_activity_id int,

    PRIMARY KEY (lecture_activity_id),
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id),
    FOREIGN KEY (student_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS subjects (
 name varchar(150) primary key,
 teacher_id int,
 lecture_id int,

 FOREIGN KEY (teacher_id) REFERENCES users(user_id),
 FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id)
);

CREATE TABLE IF NOT EXISTS group_subjects (
 group_id integer,
 subject_name varchar(150),

 PRIMARY KEY (group_id, subject_name),
 FOREIGN KEY (group_id) REFERENCES groups(group_id),
 FOREIGN KEY (subject_name) REFERENCES subjects(name)
);

CREATE TABLE IF NOT EXISTS teacher_subjects (
 user_id integer,
 subject_name varchar(150),

 PRIMARY KEY (user_id, subject_name),
 FOREIGN KEY (user_id) REFERENCES users(user_id),
 FOREIGN KEY (subject_name) REFERENCES subjects(name)
);

create table if not exists university_subject (
    id serial primary key,
    subject_name varchar(150), 
    lecture_id int,
    
    FOREIGN KEY (subject_name) REFERENCES subjects(name),
    FOREIGN KEY (lecture_id) REFERENCES lectures(lecture_id)
);

create table if not exists universities (
    id serial primary key,
    name varchar(250),
    city varchar(250),
    count_staff integer,
    year integer
);
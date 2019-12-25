CREATE TABLE "users_table"(
	user_fullname varchar(50),
	user_email varchar(50) NOT NULL PRIMARY KEY,
	user_password varchar(25),
	user_faculty varchar(10)
);

CREATE TABLE "questions_table"(
	question_id int NOT NULL PRIMARY KEY,
	questions varchar(100),
	type_question varchar(10)
);

CREATE TABLE "questionnaire_table"(
	questionnaire_id int NOT NULL PRIMARY KEY,
	user_faculty varchar(10),
	question_id_fk int NOT NULL PRIMARY KEY,
	FOREIGN KEY (question_id_fk) REFERENCES questions_table(question_id)
);
	
CREATE TABLE "answer_table"(
	answer_id int NOT NULL PRIMARY KEY,
	answer_for_question varchar(20),
	user_faculty varchar(10),
	student_id_fk varchar(50),
	question_id_fk int,
	FOREIGN KEY (student_id_fk) REFERENCES users_table(user_email),
	FOREIGN KEY (question_id_fk) REFERENCES questions_table(question_id)
);


DROP TABLE "answer_table";
DROP TABLE "questionnaire_table";
DROP TABLE "questions_table";
DROP TABLE "users_table";
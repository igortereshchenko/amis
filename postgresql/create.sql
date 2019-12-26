CREATE TABLE Groups(code text);
ALTER TABLE Groups
ADD CONSTRAINT code_pk PRIMARY KEY (code);

CREATE TABLE Subjects(name text);
ALTER TABLE Subjects
ADD CONSTRAINT name_pk PRIMARY KEY(name);

CREATE TABLE Subjects_Marks(subj_name text, curr_max_mark numeric NOT NULL,
						  actual_date DATE);
ALTER TABLE Subjects_Marks
ADD CONSTRAINT time_name_pk PRIMARY KEY(actual_date, subj_name),
ADD CONSTRAINT name_fk FOREIGN KEY(subj_name) REFERENCES Subjects(name);

CREATE TABLE Students(first_name text NOT NULL, last_name text NOT NULL,
					  study_book text, group_code text);					 
ALTER TABLE Students
ADD CONSTRAINT group_spooky_bk PRIMARY KEY(group_code, study_book),
ADD CONSTRAINT group_code_fk FOREIGN KEY(group_code) REFERENCES Groups(code);

CREATE TABLE StudentStatus(group_code text, study_book text, status text,
						   destiny text, actual_date DATE);
ALTER TABLE StudentStatus
ADD CONSTRAINT time_spooky_bk PRIMARY KEY(group_code, study_book, actual_date),
ADD CONSTRAINT group_spooky_fk FOREIGN KEY(group_code, study_book) REFERENCES Students(group_code, study_book);

CREATE TABLE SubjectSheet(subj_name text, group_code text, study_book text,
						  date_of_mark DATE, mark numeric);
ALTER TABLE SubjectSheet
ADD CONSTRAINT time_group_spooky_subj_bk PRIMARY KEY(subj_name, group_code,
											   study_book, date_of_mark),
ADD CONSTRAINT subj_name_fk FOREIGN KEY(subj_name) REFERENCES Subjects(name),
ADD CONSTRAINT group_spooky_fk FOREIGN KEY(group_code, study_book) REFERENCES Students(group_code, study_book);

CREATE TABLE Group_Subject(year int, semester int, group_code text, subj_name text);
ALTER TABLE Group_Subject
ADD CONSTRAINT group_subj_time_pk PRIMARY KEY(group_code, subj_name, year, semester),
ADD	CONSTRAINT group_code_fk FOREIGN KEY (group_code) REFERENCES Groups(code),
ADD	CONSTRAINT subj_name_fk FOREIGN KEY (subj_name) REFERENCES Subjects(name);
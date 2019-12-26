INSERT INTO public."Teacher"(
	Name, Degree)
	VALUES ('Pavlo Borisenko', 'doctor');
INSERT INTO public."Teacher"(
	Name, Degree)
	VALUES ('Tatiana Ladogubets', 'professor');
INSERT INTO public."Teacher"(
	Name, Degree)
	VALUES ('Volodimir Malchikov', 'professor');

INSERT INTO public."Discipline"(
	Name, Teacher_name)
	VALUES ('OOP', 'Pavlo Borisenko');
INSERT INTO public."Discipline"(
	Name, Teacher_name)
	VALUES ('Mathematical model', 'Pavlo Borisenko');
INSERT INTO public."Discipline"(
	Name, Teacher_name)
	VALUES ('Calculus', 'Volodimir Malchikov');
	
INSERT INTO public."Student"(
	Name, SGroup)
	VALUES ('Mozgovoy Nikita', 61);
INSERT INTO public."Student"(
	Name, SGroup)
	VALUES ('Eugene Patrushev', 62);
INSERT INTO public."Student"(
	Name, SGroup)
	VALUES ('Anna Challa', 61);

INSERT INTO public."Task"(
	ID, Discipline_name,Value, Deadline, Name)
	VALUES (0, 'OOP',15,  '2019-06-22 19:10:25-07','Do something');
INSERT INTO public."Task"(
	ID, Discipline_name,Value, Deadline, Name)
	VALUES (1, 'Calculus',20, '2019-06-30 9:10:25-07','Dont do something');
INSERT INTO public."Task"(
	ID, Discipline_name,Value, Deadline, Name)
	VALUES (2, 'OOP',10,'2019-09-24 19:10:25-07','Probably do something');

INSERT INTO public."Student_Discipline"(
	Discipline_name, Student_name, Student_group, Points)
	VALUES ('OOP', 'Mozgovoy Nikita', 61, 95);
INSERT INTO public."Student_Discipline"(
	Discipline_name, Student_name, Student_group, Points)
	VALUES ('Calculus', 'Eugene Patrushev', 62, 95);
INSERT INTO public."Student_Discipline"(
	Discipline_name, Student_name, Student_group, Points)
	VALUES ('Mathematical model', 'Anna Challa', 61, 100);

INSERT INTO public."Student_Task"(
	Student_name, Student_group, Task_id)
	VALUES ('Eugene Patrushev', 62, 1);
INSERT INTO public."Student_Task"(
	Student_name, Student_group, Task_id)
	VALUES ('Anna Challa', 61, 1);
INSERT INTO public."Student_Task"(
	Student_name, Student_group, Task_id)
	VALUES ('Mozgovoy Nikita', 61, 2);

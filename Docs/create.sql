-- Table: public."Teacher"

-- DROP TABLE public."Teacher";

CREATE TABLE public."Teacher"
(
    Name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    Degree character varying(255) COLLATE pg_catalog."default" NOT NULL
);

ALTER TABLE public."Teacher" ADD PRIMARY KEY (Name);
TABLESPACE "Test";

-- Table: public."Discipline"

-- DROP TABLE public."Discipline";

CREATE TABLE public."Discipline"
(
    Name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    Teacher_name character varying(255) COLLATE pg_catalog."default" NOT NULL
);

ALTER TABLE public."Discipline" ADD PRIMARY KEY (Name);
ALTER TABLE public."Discipline" ADD CONSTRAINT "Discipline_fk" FOREIGN KEY (Teacher_name) REFERENCES public."Teacher" (Name); 
TABLESPACE "Test";


-- Table: public."Student"

-- DROP TABLE public."Student";

CREATE TABLE public."Student"
(
    Name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    SGroup integer NOT NULL
);

ALTER TABLE public."Student" ADD PRIMARY KEY (Name, SGroup);
TABLESPACE "Test";

-- Table: public."Task"

-- DROP TABLE public."Task";

CREATE TABLE public."Task"
(
    ID integer NOT NULL,
    Discipline_name character varying(255) COLLATE pg_catalog."default",
    Value integer NOT NULL,
    Deadline time without time zone NOT NULL,
    Name character varying(255) COLLATE pg_catalog."default" NOT NULL
);

ALTER TABLE public."Task" ADD PRIMARY KEY (ID);
ALTER TABLE public."Task" ADD CONSTRAINT "Task_fk" FOREIGN KEY (Discipline_name) REFERENCES public."Discipline" (Name); 
TABLESPACE "Test";


-- Table: public."Student_Task"

-- DROP TABLE public."Student_Task";

CREATE TABLE public."Student_Task"
(
    Student_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    Student_group integer NOT NULL,
    Task_id integer NOT NULL
);

ALTER TABLE public."Student_Task" ADD PRIMARY KEY (Student_name,Student_group,Task_id);
ALTER TABLE public."Student_Task" ADD CONSTRAINT "ST_Student_fk" FOREIGN KEY (Student_group, Student_name) REFERENCES public."Student" (SGroup, Name); 
ALTER TABLE public."Student_Task" ADD CONSTRAINT "ST_Task_fk" FOREIGN KEY (Task_id) REFERENCES public."Task" (ID); 

TABLESPACE "Test";

-- Table: public."Student_Discipline"

-- DROP TABLE public."Student_Discipline";

CREATE TABLE public."Student_Discipline"
(
    Discipline_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    Student_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    Student_group integer NOT NULL,
    Points integer NOT NULL
);

ALTER TABLE public."Student_Discipline" ADD PRIMARY KEY (Discipline_name,Student_name,Student_group);
ALTER TABLE public."Student_Discipline" ADD CONSTRAINT "SD_Discipline_fk" FOREIGN KEY (Discipline_name) REFERENCES public."Discipline" (Name); 
ALTER TABLE public."Student_Discipline" ADD CONSTRAINT "SD_Student_fk" FOREIGN KEY (Student_group, Student_name) REFERENCES public."Student" (SGroup, Name); 


TABLESPACE "Test";

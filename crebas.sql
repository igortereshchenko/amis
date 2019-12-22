/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     06.12.2019 19:55:37                          */
/*==============================================================*/


drop index "performer has an album_FK";

drop index Album_PK;

drop table Album;

drop index Genre_PK;

drop table Genre;

drop index "melody has genre_FK";

drop index Melody_PK;

drop table Melody;

drop index Performer_PK;

drop table Performer;

drop index Student_PK;

drop table Student;

drop index Relationship_3_FK;

drop index "Student makes wish_FK";

drop index Wish_PK;

drop table Wish;

/*==============================================================*/
/* Table: Album                                                 */
/*==============================================================*/
create table Album (
   performer_id         INT4                 not null,
   album_title          VARCHAR(30)          not null,
   album_id             INT4                 not null,
   constraint PK_ALBUM primary key (album_id), 
	constraint unq_alb unique(album_title, performer_id)
);

/*==============================================================*/
/* Index: Album_PK                                              */
/*==============================================================*/
create unique index Album_PK on Album (
album_id
);

/*==============================================================*/
/* Index: "performer has an album_FK"                           */
/*==============================================================*/
create  index "performer has an album_FK" on Album (
performer_id
);

/*==============================================================*/
/* Table: Genre                                                 */
/*==============================================================*/
create table Genre (
   genre_name           VARCHAR(15)          not null,
   psychotype           VARCHAR(25)          not null,
   constraint PK_GENRE primary key (genre_name)
);

/*==============================================================*/
/* Index: Genre_PK                                              */
/*==============================================================*/
create unique index Genre_PK on Genre (
genre_name
);

/*==============================================================*/
/* Table: Melody                                                */
/*==============================================================*/
create table Melody (
   melody_title         VARCHAR(15)          not null,
   melody_singer        VARCHAR(25)          not null,
   melody_release_date  DATE                 not null,
   melody_genre         VARCHAR(15)          not null,
   Alb_album_id         INT4                 not null,
   melody_id            INT4                 not null,
   constraint PK_MELODY primary key (melody_id), 
	constraint unq_melody unique(melody_title, melody_singer)
);

/*==============================================================*/
/* Index: Melody_PK                                             */
/*==============================================================*/
create unique index Melody_PK on Melody (
melody_id
);

/*==============================================================*/
/* Index: "melody has genre_FK"                                 */
/*==============================================================*/
create  index "melody has genre_FK" on Melody (
melody_genre
);

/*==============================================================*/
/* Table: Performer                                             */
/*==============================================================*/
create table Performer (
   performer_name       VARCHAR(25)          not null,
   performer_id         INT4                 not null,
   constraint PK_PERFORMER primary key (performer_id), 
constraint unq_performer unique(performer_name)
);

/*==============================================================*/
/* Index: Performer_PK                                          */
/*==============================================================*/
create unique index Performer_PK on Performer (
performer_id
);

/*==============================================================*/
/* Table: Student                                               */
/*==============================================================*/
create table Student (
   faculty              VARCHAR(50)          not null,
   "group"              VARCHAR(8)           not null,
   surname              VARCHAR(15)          not null,
   name                 VARCHAR(15)          not null,
   username             VARCHAR(40)          not null,
   student_id           INT4                 not null,
   constraint PK_STUDENT primary key (student_id),
	constraint unq_student unique(faculty, "group", surname, name, username)
);

/*==============================================================*/
/* Index: Student_PK                                            */
/*==============================================================*/
create unique index Student_PK on Student (
student_id
);

/*==============================================================*/
/* Table: Wish                                                  */
/*==============================================================*/
create table Wish (
   student_id           INT4                 not null,
   wish_date            DATE                 not null,
   nickname             VARCHAR(40)          not null,
   wish_performer       VARCHAR(25)          not null,
   wish_melody          VARCHAR(20)          not null,
   wish_genre           VARCHAR(15)          not null,
   wish_id              INT4                 not null,
   constraint PK_WISH primary key (wish_id)
);

/*==============================================================*/
/* Index: Wish_PK                                               */
/*==============================================================*/
create unique index Wish_PK on Wish (
wish_id
);

/*==============================================================*/
/* Index: "Student makes wish_FK"                               */
/*==============================================================*/
create  index "Student makes wish_FK" on Wish (
student_id
);

/*==============================================================*/
/* Index: Relationship_3_FK                                     */
/*==============================================================*/
create  index Relationship_3_FK on Wish (
wish_melody
);

alter table Album
   add constraint FK_ALBUM_PERFORMER_PERFORME foreign key (performer_id)
      references Performer (performer_id)
      on delete restrict on update restrict;

alter table Melody
   add constraint "FK_MELODY_ALBUM CON_ALBUM" foreign key (Alb_album_id)
      references Album (album_id)
      on delete restrict on update restrict;

alter table Melody
   add constraint "FK_MELODY_MELODY HA_GENRE" foreign key (melody_genre)
      references Genre (genre_name)
      on delete restrict on update restrict;

alter table Wish
   add constraint FK_WISH_RELATIONS_MELODY foreign key (wish_melody)
      references Melody (melody_id)
      on delete restrict on update restrict;

alter table Wish
   add constraint "FK_WISH_STUDENT M_STUDENT" foreign key (student_id)
      references Student (student_id)
      on delete restrict on update restrict;


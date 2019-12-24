CREATE TABLE users (
    username VARCHAR(50) NOT NULL,
    password VARCHAR(64) NOT NULL,
    isAdmin BOOLEAN NOT NULL DEFAULT FALSE
);

ALTER TABLE users ADD CONSTRAINT username_pk PRIMARY KEY (username);

CREATE TABLE files (
    id UUID NOT NULL,
    createdByFk VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    createdOn TIMESTAMP
);

ALTER TABLE files ADD CONSTRAINT files_id_pk PRIMARY KEY (id);
ALTER TABLE files ADD CONSTRAINT files_createdByFk_users FOREIGN KEY (createdByFk) references users (username);

CREATE TABLE filePages (
    id UUID NOT NULL,
    fileIdFk UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    createdOn TIMESTAMP
);

ALTER TABLE filePages ADD CONSTRAINT filePages_id_pk PRIMARY KEY (id);
ALTER TABLE filePages ADD CONSTRAINT filePages_fileIdFk_files FOREIGN KEY (fileIdFk) references files (id);

CREATE TABLE fileColumns (
    id UUID NOT NULL,
    filePageIdFk UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    type varchar(50) NOT NULL,
    createdOn TIMESTAMP
);

ALTER TABLE fileColumns ADD CONSTRAINT fileColumns_id_pk PRIMARY KEY (id);
ALTER TABLE fileColumns ADD CONSTRAINT fileColumns_filePageIdFk_filePages FOREIGN KEY (filePageIdFk) references filePages (id);


CREATE TABLE schemas (
    id UUID NOT NULL,
    createdByFk VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    createdOn TIMESTAMP
);

ALTER TABLE schemas ADD CONSTRAINT schemas_id_pk PRIMARY KEY (id);
ALTER TABLE schemas ADD CONSTRAINT schemas_createdByFk_users FOREIGN KEY (createdByFk) references users (username);

CREATE TABLE entities (
    id UUID NOT NULL,
    schemaIdFk UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    isOverrideExisted BOOLEAN NOT NULL DEFAULT FALSE,
    createdOn TIMESTAMP
);

ALTER TABLE entities ADD CONSTRAINT entities_id_pk PRIMARY KEY (id);
ALTER TABLE entities ADD CONSTRAINT entities_schemaIdFk_schemas FOREIGN KEY (schemaIdFk) references schemas (id);

CREATE TABLE attributes (
    id UUID NOT NULL,
    entityIdFk UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    isNull BOOLEAN NOT NULL DEFAULT TRUE,
    isPrimaryKey BOOLEAN NOT NULL DEFAULT FALSE,
    createdOn TIMESTAMP
);

ALTER TABLE attributes ADD CONSTRAINT attributes_id_pk PRIMARY KEY (id);
ALTER TABLE attributes ADD CONSTRAINT attributes_entityIdFk_entity FOREIGN KEY (entityIdFk) references entities (id);
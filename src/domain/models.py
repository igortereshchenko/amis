from datetime import datetime
from uuid import uuid4

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from forms.attributes import AttributeViewModel
from forms.entities import EntityForm
from forms.schemas import SchemaForm

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = "users"

    Username = db.Column("username", db.String, primary_key=True)
    Password = db.Column("password", db.String, nullable=False)
    IsAdmin = db.Column("isAdmin", db.Boolean, nullable=False, default=False)

    def get_id(self):
        return self.Username


class Files(db.Model):
    __tablename__ = "files"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    CreatedByFK = db.Column("createdByFk", db.String, db.ForeignKey("users.username"))
    CreatedBy = db.relationship("Users", backref=backref("Files", cascade="all,delete"), passive_deletes="True")


class FilePages(db.Model):
    __tablename__ = "filePages"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    FileIdFk = db.Column("fileIdFk", UUID(as_uuid=True), db.ForeignKey("files.id"))
    File = db.relationship("Files", backref=backref('Pages', cascade='all,delete'), passive_deletes=True)


class FileColumns(db.Model):
    __tablename__ = "fileColumns"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    Type = db.Column("type", db.String, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    FilePageIdFk = db.Column("filePageIdFk", UUID(as_uuid=True), db.ForeignKey("filePages.id"))
    FilePage = db.relationship("FilePages", backref=backref('Columns', cascade='all,delete'), passive_deletes=True)


class Schemas(db.Model):
    __tablename__ = "schemas"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    CreatedByFK = db.Column("createdByFk", db.String, db.ForeignKey("users.username"))
    CreatedBy = db.relationship("Users", backref=backref("Schemas", cascade="all,delete"), passive_deletes="True")

    def wtf(self):
        return SchemaForm(
            Id=self.Id,
            Name=self.Name,
            CreatedOn=self.CreatedOn
        )

    def map_from(self, form):
        self.Name = form.Name.data


class Entities(db.Model):
    __tablename__ = "entities"

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    IsOverrideExisted = db.Column("isOverrideExisted", db.Boolean, nullable=False, default=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    SchemaIdFk = db.Column("schemaIdFk", UUID(as_uuid=True), db.ForeignKey("schemas.id"))
    Schema = db.relationship("Schemas", backref=backref('Entities', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return EntityForm(
            Id=self.Id,
            Name=self.Name,
            IsOverrideExisted=self.IsOverrideExisted,
            CreatedOn=self.CreatedOn,
            Schema=self.SchemaIdFk
        )

    def map_from(self, form):
        self.Name = form.Name.data
        self.IsOverrideExisted = form.IsOverrideExisted.data
        self.SchemaIdFk = form.Schema.data


class Attributes(db.Model):
    __tablename__ = "attributes"

    def __init__(self, name, type, is_null, is_pk):
        self.Name = name
        self.Type = type
        self.IsNull = is_null
        self.IsPrimaryKey = is_pk

    Id = db.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4)
    Name = db.Column("name", db.String, nullable=False)
    Type = db.Column("type", db.String, nullable=False)
    IsNull = db.Column("isNUll", db.Boolean, nullable=False, default=True)
    IsPrimaryKey = db.Column("isPrimaryKey", db.Boolean, nullable=False, default=False)
    CreatedOn = db.Column("createdOn", db.TIMESTAMP, default=datetime.utcnow)

    EntityIdFk = db.Column("entityIdFk", UUID(as_uuid=True), db.ForeignKey("entities.id"))
    Entity = db.relationship("Entities", backref=backref('Attributes', cascade='all,delete'), passive_deletes=True)

    def wtf(self):
        return AttributeViewModel(
            Name=self.Name,
            Type=self.Type,
            IsNull=self.IsNull,
            IsPrimaryKey=self.IsPrimaryKey,
            CreatedOn=self.CreatedOn,
            Entity=self.EntityIdFk
        )

    def map_from(self, form):
        self.Name = form.Name.data
        self.Type = form.Type.data
        self.IsNull = form.IsNull.data
        self.IsPrimaryKey = form.IsPrimaryKey.data
        self.EntityIdFk = form.Entity.data

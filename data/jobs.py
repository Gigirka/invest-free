import datetime
import sqlalchemy
from flask_wtf.file import FileField
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)

    project_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime,
                                   default=datetime.datetime.now)
    needed_money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    invested_money = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # user = orm.relationship('User')

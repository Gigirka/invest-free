import datetime
import sqlalchemy
# from flask_login import UserMixin
from flask_login import UserMixin
from flask_wtf.file import FileField
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)

    image = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)

    money = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    personal = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capital = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    private_or_fund = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # jobs = orm.relationship("Jobs", back_populates='user')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

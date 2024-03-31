import datetime
import sqlalchemy
# from flask_login import UserMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    money = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    exp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    exp = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    personal = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    capital = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    qualification = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    private_or_fund = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    money = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    jobs = orm.relationship("Jobs", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

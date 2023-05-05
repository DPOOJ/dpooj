from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import time
from flask import Flask
from init import db


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(60))
    balance=db.Column(db.Integer) 
    is_uploaded = db.Column(db.Integer)   
    is_started = db.Column(db.Integer)   
    is_wrong = db.Column(db.Integer)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Validation_code(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60))
    code = db.Column(db.String(6))
    password_hash = db.Column(db.String(128))
    last_time = db.Column(db.Float)
    
    def set_code(self, code):
        self.password_hash = generate_password_hash(code)
        self.last_time = time.time()

    def validate_code(self, code):
        return check_password_hash(self.password_hash, code)
    
class IPinfo(db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    ip=db.Column(db.String(50))
    tries=db.Column(db.Integer)
    last_time=db.Column(db.Float)
    
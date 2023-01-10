from . import db
from flask_login import UserMixin
import sqlalchemy
from sqlalchemy import ForeignKey

class Account(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    alias = db.Column(db.String(150))
    
class Trackers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_name = db.Column(db.String(15))
    t_type = db.Column(db.Integer) #Check Numeric or Boolean
    t_note = db.Column(db.String(150))
    t_date = db.Column(db.DateTime(timezone=True), default = sqlalchemy.sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    
class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_value = db.Column(db.Integer)
    t_date = db.Column(db.DateTime(timezone=True), default = sqlalchemy.sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    t_id = db.Column(db.Integer, db.ForeignKey('trackers.id'))


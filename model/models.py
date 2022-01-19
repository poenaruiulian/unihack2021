from manager.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    mail = db.Column(db.Text, nullable=False)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    mail = db.Column(db.Text, nullable=False)
    subject = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    perc_50 = db.Column(db.Integer, nullable=False)
    perc_70 = db.Column(db.Integer, nullable=False)
    perc_100 = db.Column(db.Integer, nullable=False)
    latit = db.Column(db.Integer, nullable=False)
    long = db.Column(db.Integer, nullable=False)

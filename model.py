import os
from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True, nullable = False)
    password = db.Column(db.String(255), nullable = False)

class Progress(db.Model):
    __tablename__ = 'progress'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    collectible_name = db.Column(db.String(255), nullable=False)
    collected = db.Column(db.Boolean, default=False)

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__=="__main__":
    from server import app
    connect_to_db(app)
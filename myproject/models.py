from myproject import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):

        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"


class Product(db.Model):

    prod_id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(64), unique=True, index=True)
    price = db.Column(db.Integer, index=True)

    def __init__(self, pname, price):

        self.pname = pname
        self.price = price

    def __repr__(self):
        return f"Product('{self.pname}','{self.price}')"


class Cart(db.Model):

    cart_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, db.ForeignKey('User.id'),
                   nullable=False)
    prod_id = db.Column(db.Integer, db.ForeignKey('Prodcut.prod_id'),
                        nullable=False)

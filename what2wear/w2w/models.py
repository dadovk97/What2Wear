from datetime import datetime
from w2w import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Closet', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Closet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    occasion = db.Column(db.String(100), nullable=True)
    waterproof = db.Column(db.Boolean, nullable=True)
    winter = db.Column(db.Boolean, nullable=True)
    spring = db.Column(db.Boolean, nullable=True)
    summer = db.Column(db.Boolean, nullable=True)
    autumn = db.Column(db.Boolean, nullable=True)
    public_closet = db.Column(db.Boolean, nullable=True)
    img_clothes = db.Column(db.String(20), nullable=True, default='hanger.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Closet('{self.item}' , '{self.color}' , '{self.occasion}' , '{self.waterproof}' , '{self.winter}' , '{self.spring}' , '{self.summer}' , '{self.autumn}', '{self.public_closet}' , '{self.img_clothes}')"
        
from datetime import datetime, date
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = "default.png")
    password = db.Column(db.String(60), nullable = False)
    goal = db.relationship('Goal', backref = 'person', lazy = True)

    def __repr__(self):
        return f"User('{self.username}', '{self.image_file}', '{self.email}')"

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.now())
    start_date = db.Column(db.Date, nullable=False, default=date.today())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    Days = db.relationship('Day', backref='goal', lazy=True)


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    breakfast = db.Column(db.Integer, nullable=False, default=0)
    breakfast_img_file = db.Column(db.String(20), nullable=False,
                                   default='default.jpg')
    lunch = db.Column(db.Integer, nullable=False, default=0)
    lunch_img_file = db.Column(db.String(20), nullable=False,
                               default='default.jpg')
    dinner = db.Column(db.Integer, nullable=False, default=0)
    dinner_img_file = db.Column(db.String(20), nullable=False,
                                default='default.jpg')
    day_date = db.Column(db.Date, nullable=False, default=date.today())
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)

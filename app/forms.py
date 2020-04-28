from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.models import User, Goal, Day

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators = [DataRequired(), Length(min = 5, max = 20)])
    email = StringField('Email', 
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                             validators = [DataRequired(), Length(min = 8, max = 20)])
    confirm_password = PasswordField('Confirm Password',
                             validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Username already exists. Choose another username.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email already exists. Login if you are already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators = [DataRequired(), Email()])
    password = PasswordField('Password',
                             validators = [DataRequired(), Length(min = 8, max = 20)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class GoalForm(FlaskForm):
    weight = IntegerField('Weight to Lose', validators=[DataRequired()])
    days = IntegerField('Days to achieve Goal', validators=[DataRequired()])
    start_date = DateField('Start Date',validators=[DataRequired()])
    submit = SubmitField('Go')

class CalculateCalorie(FlaskForm):
    picture = FileField('Add food item to check calorie', validators=[
                        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Check')

class DayForm(FlaskForm):
    breakfast_pic = FileField('Breakfast', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'])])
    lunch_pic = FileField('Lunch', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'])])
    dinner_pic = FileField('Dinner', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Go')

import os
import secrets
from PIL import Image
from datetime import datetime, date
from flask import render_template, flash, url_for, current_app, redirect, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, GoalForm, CalculateCalorie, DayForm
from app.models import User, Goal, Day
from app.utils import save_picture1
from flask_login import login_user, current_user, logout_user, login_required
import app.Predict_Calories as pc

@app.route('/')
def landing():
    return render_template("landing.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/check_calorie', methods = ['GET', 'POST'])
def check_calorie():
    form = CalculateCalorie()
    p_class = None
    p_img = None
    p_cal = None
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture1(form.picture.data)
            # predict picture using ml model
            p_img = "C:/Users/Dell/Desktop/OST_Project/Calorimeter/app/static/food_pics/" + format(picture_file)
            p_class = pc.predict_class(p_img)
            p_cal = pc.predict_cal(p_class)
    return render_template('check_calorie.html', form=form, title='Check Calorie', p_class=p_class, p_img=p_img, your_cal = p_cal)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!! You can login now', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        name = current_user.username
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/goal", methods=['GET'])
@login_required
def display_goal():
    goal = Goal.query.filter_by(person=current_user).first()
    if goal:
        date_today = date.today()
        diff = (date_today - goal.start_date).days
        return render_template('goal.html', goal=goal, diff=diff)
    else:
        return render_template('goal.html')


@app.route("/goal/new", methods=['GET', 'POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(weight=form.weight.data, days=form.days.data, start_date=form.start_date.data,
                    person=current_user)
        db.session.add(goal)
        db.session.commit()
        flash('Your Goal has been created!', 'success')
        return redirect(url_for('display_goal'))
    return render_template('add_goal.html', title='New Goal', form=form, legend='New Goal')


@app.route("/goal/<int:goal_id>/update", methods=['GET', 'POST'])
@login_required
def update_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    form = GoalForm()
    if form.validate_on_submit():
        goal.weight = form.weight.data
        goal.days = form.days.data
        goal.start_date = form.start_date.data
        db.session.commit()
        flash('Your Goal has been updated', 'success')
        return redirect(url_for('display_goal'))
    elif request.method == 'GET':
        form.weight.data = goal.weight
        form.days.data = goal.days
        form.start_date.data = goal.start_date
    return render_template('add_goal.html', title='Update Goal', form=form,
                           legend='Update Goal')


@app.route("/goal/<int:goal_id>/delete", methods=['POST'])
@login_required
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    days = Day.query.filter_by(goal = goal)
    for day in days:
        db.session.delete(day)
    db.session.delete(goal)
    db.session.commit()
    flash('Your Goal has been deleted', 'success')
    return redirect(url_for('display_goal'))


@app.route('/goal/<int:goal_id>/day/', methods = ['GET', 'POST'])
@login_required
def day(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    date_today = date.today()
    diff = (date_today - goal.start_date).days
    day = Day.query.filter_by(day_date=date.today()).first()
    if day == None:
        day = Day(goal=goal)
        db.session.add(day)
        db.session.commit()

    form = DayForm()
    
    if form.validate_on_submit():
        if form.breakfast_pic.data:
            pf = save_picture1(form.breakfast_pic.data)
            day.breakfast_img_file = pf
            p_img = "C:/Users/Dell/Desktop/OST_Project/Calorimeter/app/static/food_pics/" + format(pf)
            p_class = pc.predict_class(p_img)
            p_cal = pc.predict_cal(p_class)
            # predict calories in breakfast, pf is the picture
            # cal = predict(pf)
            day.breakfast = p_cal

        if form.lunch_pic.data:
            pf = save_picture1(form.lunch_pic.data)
            day.lunch_img_file = pf
            p_img = "C:/Users/Dell/Desktop/OST_Project/Calorimeter/app/static/food_pics/" + format(pf)
            p_class = pc.predict_class(p_img)
            p_cal = pc.predict_cal(p_class)
            # predict calories in lunch, pf is the picture
            day.lunch = p_cal

        if form.dinner_pic.data:
            pf = save_picture1(form.dinner_pic.data)
            day.dinner_img_file = pf
            p_img = "C:/Users/Dell/Desktop/OST_Project/Calorimeter/app/static/food_pics/" + format(pf)
            p_class = pc.predict_class(p_img)
            p_cal = pc.predict_cal(p_class)
            # predict calories in dinner, pf is the picture
            # cal = predict(pf)
            day.dinner = p_cal

        db.session.commit()
        flash('Meal for the day updated successfully', 'success')
        return redirect(url_for('day', goal_id=goal.id))
    
    b_img = url_for('static', filename='food_pics/' +
                    day.breakfast_img_file)
    l_img = url_for('static', filename='food_pics/' +
                    day.lunch_img_file)
    d_img = url_for('static', filename='food_pics/' +
                    day.dinner_img_file)
    return render_template('day.html', goal=goal, diff=diff, day=day, b_img=b_img, l_img=l_img, d_img=d_img, form=form)

@app.route('/goal/<int:goal_id>/days/view', methods = ['GET'])
@login_required
def display_days(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if goal.person != current_user:
        abort(403)
    days = Day.query.filter_by(goal=goal)

    return render_template('all_days.html', days=days, goal=goal)
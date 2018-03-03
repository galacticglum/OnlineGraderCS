from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user
from grader import app, db
from grader.forms import LoginForm, RegisterForm
from grader.models.user import User

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/register', methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    print(form.errors)
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('register.html', form = form)

@app.route('/login', methods = ["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first_or_404()
        if user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

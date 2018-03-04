from flask import render_template, redirect, url_for
from flask_user import login_required
from grader import app

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/members')
@login_required
def members_page():
    return render_template('members.html')

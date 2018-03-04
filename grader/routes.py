from flask import render_template, redirect, url_for, request
from flask_user import login_required, roles_required
from grader import app, db
from grader.models.contest import Contest
from grader.forms import AddContestForm

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/members')
@login_required
def members_page():
    return render_template('members.html')

@app.route('/dashboard')
@roles_required('Admin')
def dashboard_page():
    contests = db.session.query(Contest)
    return render_template('dashboard.html', contests=contests)

@app.route('/dashboard/add_contest', methods=['GET', 'POST'])
@roles_required('Admin')
def dashboard_add_contest_page():
    form = AddContestForm(request.form)
    if request.method == 'POST' and form.validate():
        contest = Contest(name=form.name.data,
                        start_time=form.start_time.data,
                        end_time=form.end_time.data)
        db.session.add(contest)
        db.session.commit()
        
        return redirect(url_for('dashboard_page'))
    return render_template('add_contest.html', form=form)

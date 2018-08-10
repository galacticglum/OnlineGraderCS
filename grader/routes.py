import os
import datetime
import threading
import tempfile
import requests

from flask import url_for, redirect, render_template, request, abort, flash, send_file, send_from_directory, jsonify, session
from flask_security import login_required, current_user

from grader import application, db, client_secret_path, google_scopes, upload_file_path
from grader.models import Contest, Problem, GoogleCredentials
from grader.utilities import run_subprocess_safe, run_testcase_compiled, run_testcase_python, \
    get_scoreboard_results, get_google_credentials, credentials_to_json, json_credentials_to_dict, \
    add_url_params

from grader.forms import SubmissionForm

import grader.pagination as pagination_lib
import google.oauth2.credentials
import google_auth_oauthlib.flow

@application.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@application.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@application.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

def get_contests():
    contests = db.session.query(Contest)

    # We need to nullify our contests query if there are no elements.
    # This is because our template checks whether the contest is null (not the length)
    if contests.count() == 0:
        contests = None

    return contests

@application.route('/')
def index():
    contests = get_contests if current_user.is_authenticated else None
    return render_template('index.html', contests=contests)

@application.route('/rules')
def rules():
    return render_template('rules.html')

@application.route('/problem/<int:problem_id>')
@login_required
def problem(problem_id):
    problem = db.session.query(Problem).filter(Problem.id == problem_id).first()
    if problem == None:
        abort(404)
        return

    participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
        .filter(ContestParticipation.contest_id == problem.contest_id).first()

    if participation_query == None:
        abort(403)
        return

    return send_file(os.path.join(upload_file_path, problem.pdf_link), attachment_filename="problem{0}.pdf".format(problem.id), mimetype="application/pdf")

@application.route('/contests')
def contests():
    contests = get_contests() 
    display_open_contests = contests != None and any(contest.is_running() for contest in contests.all())

    return render_template('contests.html', contests=contests, display_open_contests=display_open_contests)

@application.route('/contest/<int:contest_id>', methods=['GET', 'POST'])
@login_required
def contest(contest_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return
        
    form = SubmissionForm()
    form.problem.choices = [(problem.id, problem.name) for problem in contest.problems]

    participation_query = db.session.query(ContestParticipation).filter(ContestParticipation.user_id == current_user.id) \
        .filter(ContestParticipation.contest_id == contest_id)

    if form.validate_on_submit():
        submission_count = db.session.query(Submission).filter(Submission.user_id == current_user.id, Submission.problem_id == form.problem.data).count()

        if (contest.has_duration_expired(participation_query.first()) and not current_user.has_role('superuser')) or submission_count > 50:
            flash('Sorry, unable to submit.', 'error')
            return redirect(url_for('contest', contest_id=contest_id))

        try:       
            source_code = request.files['file'].read().decode('utf-8-sig')
        except:
            flash('Unable to submit, could not read file. Make sure that you are uploading the text file containing your source code. Valid file endings include: ".cs", ".py", and ".java".', 'error')
            return redirect(url_for('contest', contest_id=contest_id))

        language_mode = int(form.language.data)
        problem = db.session.query(Problem).filter(Problem.id == form.problem.data).first()

        temp_dir = tempfile.mkdtemp()
        temp_exec_file = None

        exec_output = None
        if language_mode != 0:
            temp_source_file = None
            temp_exec_file = None
            suffix = str()

            if language_mode == 2:
                suffix = ".java"
            else:
                temp_exec_file = tempfile.NamedTemporaryFile(dir=temp_dir, delete=False)
                temp_exec_file.close()

            temp_source_file = tempfile.NamedTemporaryFile(dir=temp_dir, mode='w', delete=False, suffix=suffix)
            temp_source_file.write(source_code)
            temp_source_file.close()

            command = []
            if language_mode == 1:
                command = ["csc", "-out:{0}".format(temp_exec_file.name), temp_source_file.name]
            elif language_mode == 2:
                command = ["javac", temp_source_file.name]

            exec_output, status = run_subprocess_safe(command)
            if status != -3:
                exec_output = None

            os.remove(temp_source_file.name)

        submission = Submission(user_id=current_user.id, problem_id=form.problem.data, time=datetime.datetime.now(), \
            code=source_code, score=0, language=language_mode, compiler_output=exec_output)

        db.session.add(submission)
        db.session.commit()

        testcases = problem.testcases.all()
        for i in range(len(testcases)):
            testcase = testcases[i]

            binary_input = testcase.input_data.encode('utf-8')
            expected_output = testcase.output_data.splitlines()

            compile_thread = None
            if language_mode == 0:
                compile_thread = threading.Thread(target=run_testcase_python, args=(source_code, binary_input, expected_output, testcase.id, \
                    submission.id, language_mode))
            else:
                do_delete = i == len(testcases) - 1

                compile_thread = threading.Thread(target=run_testcase_compiled, args=(binary_input, expected_output, testcase.id, submission.id, \
                    language_mode, (temp_exec_file.name if language_mode == 1 else temp_dir), do_delete))
            
            compile_thread.start()

        return redirect(url_for('submission', submission_id=submission.id))
    else:
        # Check if the contest has expired or if it hasn't started yet
        if not contest.is_running() and not current_user.has_role('superuser'):
            flash('Sorry, the contest you are trying to join is closed.', 'error')
            return redirect(url_for('index'))

        already_joined = participation_query.count() > 0

        if not already_joined:
            contest_participation = ContestParticipation(user_id=current_user.id, contest_id=contest_id, \
                join_time=datetime.datetime.now())
                
            db.session.add(contest_participation)
            db.session.commit()

            flash('Successfully joined {0}!'.format(contest.name))
        else:
            contest_participation = participation_query.first()

        time_left = contest_participation.join_time + datetime.timedelta(minutes=contest.duration_minutes) - datetime.datetime.now()

        submissions = []
        most_recent_submissions = {}
        highest_scoring_submissions = {}

        for problem in contest.problems:
            most_recent_submissions[problem] = db.session.query(Submission).filter(Submission.user_id == current_user.id, \
                Submission.problem_id == problem.id).order_by(Submission.time.desc()).first()

            highest_scoring_submissions[problem] = db.session.query(Submission).filter(Submission.user_id == current_user.id, \
                Submission.problem_id == problem.id).order_by(Submission.score.desc()).first()

            for submission in db.session.query(Submission).filter(Submission.user_id == current_user.id, Submission.problem_id == problem.id) \
                .order_by(Submission.time.desc()).all():
                submissions.append((problem, submission))

        can_submit = not contest.has_duration_expired(participation_query.first()) or current_user.has_role('superuser')
        return render_template('contest.html', contest=contest, submissions=submissions, time_left=time_left.total_seconds(), \
            submission_form=form, can_submit=can_submit, most_recent_submissions=most_recent_submissions, \
            highest_scoring_submissions=highest_scoring_submissions)

@application.route('/scoreboard/<int:contest_id>')
@login_required
def scoreboard(contest_id):
    if not current_user.has_role('superuser'):
        abort(403)
        return

    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    return render_template('scoreboard.html', contest=contest, scores=get_scoreboard_results(contest_id))

@application.route('/scoreboard/results/<int:contest_id>')
@login_required
def scoreboard_results(contest_id):
    if not current_user.has_role('superuser'):
        abort(403)
        return

    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    # If the contest doesn't exist, we show a 404 error.
    if contest == None:
        abort(404)
        return

    is_contest_closed = contest.has_expired()
    return jsonify(scores=get_scoreboard_results(contest_id), closed=is_contest_closed)

@application.route('/submission/<int:submission_id>')
@login_required
def submission(submission_id):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission == None:
        abort(404)
        return

    if submission.user_id != current_user.id and not current_user.has_role('superuser'):
        abort(403)
        return
 
    problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
    contest = db.session.query(Contest).filter(Contest.id == problem.contest_id).first()

    tests = []
    for testcase in problem.testcases:
        test_run = db.session.query(TestRun).filter(TestRun.testcase_id == testcase.id, TestRun.submission_id == submission_id).first()
        tests.append((testcase, test_run))

    return render_template('submission.html', submission=submission, contest=contest, problem=problem, tests=tests)

@application.route('/submission/results/<int:submission_id>')
@login_required
def submission_results(submission_id):
    submission = db.session.query(Submission).filter(Submission.id == submission_id).first()
    if submission == None:
        abort(404)
        return

    if submission.user_id != current_user.id and not current_user.has_role('superuser'):
        abort(403)
        return
 
    problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
    #contest = db.session.query(Contest).filter(Contest.id == problem.contest_id).first()

    tests = []
    for testcase in problem.testcases:
        test_run = db.session.query(TestRun).filter(TestRun.testcase_id == testcase.id, TestRun.submission_id == submission_id).first()
        result_object = {}
        result_object['id'] = testcase.id
        result_object['status'] = test_run.status if test_run != None else 0
        result_object['status_name'] = 'None' if test_run == None else test_run.get_status_name()
        result_object['output'] = '' if test_run == None or test_run.output == None else test_run.output
        tests.append(result_object)

    return jsonify(tests)

@application.route('/settings')
def settings():
    return render_template('settings.html')

@application.route('/authenticate/drive')
def authenticate_drive():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secret_path, scopes=google_scopes)
    flow.redirect_uri = url_for('authenticate_drive_callback', _external=True)

    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    session['state'] = state

    return redirect(authorization_url)

@application.route('/authenticate/drive/oauth2callback')
def authenticate_drive_callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(client_secret_path, scopes=google_scopes, state=state)
    flow.redirect_uri = url_for('authenticate_drive_callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials_query = get_google_credentials()
    if credentials_query == None:
        # Store credentials
        credentials = GoogleCredentials(user_id=current_user.id, credentials_json=credentials_to_json(flow.credentials))
        db.session.add(credentials)
    else:
        credentials_query.credentials_json = credentials_to_json(flow.credentials)

    db.session.commit()

    return redirect(url_for('settings'))

@application.route('/authenticate/drive/revoke')
def revoke_drive_authentication():
    user_google_credentials = get_google_credentials()
    if user_google_credentials == None:
        abort(403)
        return

    credentials = google.oauth2.credentials.Credentials(**json_credentials_to_dict(user_google_credentials.credentials_json))

    revoke = requests.post('https://accounts.google.com/o/oauth2/revoke', \
        params={'token': credentials.token}, \
        headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        flash('Google credentials successfully revoked.', 'success')
    else:
        flash('An error occurred revoking Google credentials.', 'error')

    GoogleCredentials.query.filter(GoogleCredentials.user_id == current_user.id).delete()
    db.session.commit()

    return redirect(url_for('settings'))

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
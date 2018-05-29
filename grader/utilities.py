import subprocess
import os
import json
import shutil

from grader import application, db
from grader.models import User, ContestParticipation, TestRun, Testcase, Problem, Contest, Submission, GoogleCredentials
from flask_security import current_user

def run_subprocess_safe(args, input_data=None, timeout=None):
    try:
        output = subprocess.check_output(args, input=input_data, timeout=timeout, stderr=subprocess.STDOUT).decode('utf-8')
        return output, 0
    except subprocess.TimeoutExpired as _:
        return None, -2
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8'), -3
        

def run_testcase_compiled(input_data, expected_output, testcase_id, submission_id, language_mode, exec_filepath, do_delete=False):
    if language_mode == 0: return

    command = str()
    if language_mode == 1:
        command = ["mono", exec_filepath]
    elif language_mode == 2:
        command = ["java", "-classpath", "{0}".format(exec_filepath), "Main"]

    output, comp_status = run_subprocess_safe(command, input_data, application.config['SCRIPT_RUN_TIMEOUT'])
    write_test_run(expected_output, output, testcase_id, submission_id, comp_status)

    if do_delete:
        dir_path = exec_filepath
        if language_mode == 1:
            dir_path = os.path.dirname(os.path.realpath(exec_filepath))
        
        shutil.rmtree(dir_path)

def run_testcase_python(source_code, input_data, expected_output, testcase_id, submission_id, language_mode):
    if language_mode != 0: return

    output, comp_status = run_subprocess_safe(["python", "-c", source_code], input_data, application.config['SCRIPT_RUN_TIMEOUT'])
    write_test_run(expected_output, output, testcase_id, submission_id, comp_status)

def write_test_run(expected_output, output, testcase_id, submission_id, comp_status):
    with application.app_context():
        correct = False
        if output != None and comp_status != -3:
            correct = Testcase.matches(expected_output, output.splitlines())

        status = comp_status if comp_status != 0 else (1 if correct else -1)
        test_run = TestRun(testcase_id=testcase_id, submission_id=submission_id, status=status, output=output if output else '')
        db.session.add(test_run)

        submission = db.session.query(Submission).with_lockmode('update').filter(Submission.id == submission_id).first()
        #problem = db.session.query(Problem).filter(Problem.id == submission.problem_id).first()
        testcase = db.session.query(Testcase).filter(Testcase.id == testcase_id).first()

        tries = 0

        # In case of a race condition or concurrent insert, we need to wait for the db to be unlocked.
        while tries < 50:
            try:
                submission.score = submission.score + (testcase.score_weight if correct else 0)
                db.session.commit()
                break
            except Exception as exec:
                db.session.rollback()

            tries += 1



def get_scoreboard_results(contest_id):
    participations = db.session.query(User, ContestParticipation).filter(ContestParticipation.contest_id == contest_id) \
        .filter(User.id == ContestParticipation.user_id).all()

    scores = []
    for participation in participations:
        if (participation[0].has_role('superuser')): continue

        total_score = get_total_score(contest_id, participation[0].id)
        result_object = {}
        result_object['user'] = get_user_full_name(participation[0].id)
        result_object['total_score'] = total_score
        scores.append(result_object)

    return sorted(scores, reverse=True, key=lambda x: x['total_score'])



def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def credentials_to_json(credentials):
    credentials_as_dict = credentials_to_dict(credentials)
    credentials_json = json.dumps(credentials_as_dict)

    return credentials_json

def json_credentials_to_dict(credentials_json): return json.loads(credentials_json)



def get_google_credentials(): return db.session.query(GoogleCredentials).filter(GoogleCredentials.user_id == current_user.id).first()

def has_authenticated_with_google():
    return get_google_credentials() != None

def get_formatted_datetime(datetime):
    return datetime.strftime('%b %d %Y, %I:%M %p')

def get_total_score(contest_id, user_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()

    total_score = 0
    for problem in contest.problems:
        highest_scoring_submission = db.session.query(Submission).filter(Submission.user_id == user_id, \
        Submission.problem_id == problem.id).order_by(Submission.score.desc()).first()

        if highest_scoring_submission != None:
            total_score += highest_scoring_submission.score

    return total_score

def get_user_full_name(user_id):
    user = db.session.query(User).filter(User.id == user_id).first()
    if user == None: return '<None: id={0}>'.format(user_id)

    return (user.first_name if user.first_name else '') + (' ' + user.last_name if user.last_name else '')

def get_problem_name(problem_id):
    problem = db.session.query(Problem).filter(Problem.id == problem_id).first()
    if problem == None: return '<None: id={0}>'.format(problem_id)

    return problem.name

def get_contest_name(contest_id):
    contest = db.session.query(Contest).filter(Contest.id == contest_id).first()
    if contest == None: return 'None: id={0}'.format(contest_id)

    return contest.name


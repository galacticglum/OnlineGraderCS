from flask_admin.contrib import sqla
import flask_admin
from grader import upload_file_path
import wtforms
from flask_security import current_user
import uuid
from flask import abort, redirect, url_for, request
from grader.utilities import get_user_full_name, get_problem_name, get_contest_name

# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

def generate_problem_file_name(object, file_data):
    return 'problem_{0}'.format(uuid.uuid4().hex)

class ProblemView(MyModelView):
    column_list = ('name','contest','total_points')
    form_overrides = {
        'pdf_link': flask_admin.form.FileUploadField
    }

    form_args = {
        'pdf_link' : {
            'label' : 'File',
            'base_path': upload_file_path,
            'allow_overwrite': False,
            'namegen': generate_problem_file_name,
            'validators':[wtforms.validators.Required()]
        }
    }

class SubmissionView(MyModelView):
    column_list = ('id', 'user_id', 'problem_id', 'time', 'language', 'score')
    form_widget_args = {
        'code' : {
            'readonly': True,
            'rows': 25
        }
    }

    column_labels = dict(user_id='User', problem_id='Problem')
    column_formatters = dict(language=lambda v, c, m, p: m.get_language_name(), 
        user_id=lambda v, c, m, p: get_user_full_name(m.user_id),
        problem_id=lambda v, c, m, p: get_problem_name(m.problem_id))

    can_create = False
    list_template = 'admin/model/submission.html'

class ContestParticipationView(MyModelView):
    column_list = ('user_id', 'contest_id')
    column_labels = dict(user_id='User', contest_id='Contest')
    column_formatters = dict(user_id=lambda v, c, m, p: get_user_full_name(m.user_id),
                            contest_id=lambda v, c, m, p: get_contest_name(m.contest_id))

    can_create = False

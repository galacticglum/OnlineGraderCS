from grader import upload_file_path
import wtforms
from flask_security import current_user
import uuid
from flask import abort, redirect, url_for, request
from grader.utilities import get_user_full_name, get_problem_name, get_contest_name

from enum import Enum
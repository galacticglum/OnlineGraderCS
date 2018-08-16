from grader import db
from grader.models import User
from grader.utilities import stdio_confirm

prompt = 'Are you sure you would like to continue? This will drop and recreate all tables in the database.'

if not stdio_confirm(prompt, resp=False):
    exit(1)

db.drop_all()
db.create_all()

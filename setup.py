# Recreates the database schema
from grader import db
import grader.models

db.drop_all()
db.create_all()

db.session.commit()
# Recreates the database schema
from app import db
import user

db.drop_all()
db.create_all()

db.session.commit()
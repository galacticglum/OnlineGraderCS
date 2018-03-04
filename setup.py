# Recreates the database schema
from grader import db
from grader import user_manager

import grader.models

db.drop_all()
db.create_all()

# Add roles
admin_role = grader.models.user.Role(name='Admin')
db.session.add(admin_role)

# Add users (testing)
db.session.add(grader.models.user.User(username='admin', password=user_manager.hash_password('Password1'), email='admin@email.com', active=True, roles=[admin_role,]))
db.session.add(grader.models.user.User(username='noadmin', password=user_manager.hash_password('Password1'), email='noadmin@email.com', active=True))

db.session.commit()
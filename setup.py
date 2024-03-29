"""
Populate a small db with some example entries.
"""

from grader import application, db, user_datastore
from grader.models import Role
from flask_security.utils import encrypt_password

db.drop_all()
db.create_all()

with application.app_context():
    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()

    test_user = user_datastore.create_user(
        first_name='Admin',
        email='admin@email.com',
        password=encrypt_password('admin'),
        roles=[user_role, super_user_role]
    )
    
    db.session.commit()

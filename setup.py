"""
Populate a small db with some example entries.
"""

import random

from grader import application, db, user_datastore
from grader.models import Role, Problem, Contest, ProblemDifficultyType
from flask_security.utils import encrypt_password

from datetime import datetime

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

    test_contest = Contest(name='Bubpart\'s Summer Contest', start_time=datetime(year=2018, day=9, month=8),
                            end_time=datetime(year=2018, day=19, month=8), duration_minutes=90,
                            problems=[Problem(name='Maximum Binary Path Sum', description='GIGGLE MY NIGGLE',
                                    points=5, difficulty=ProblemDifficultyType.easy)])

    TEST_PROBLEM_DESCRIPTION = 'Some collapsible content. Click the button to toggle between showing and hiding \
                                the collapsible content. Lorem ipsum dolor sit amet, consectetur adipisicing elit\
                                , sed do eiusmod'

    for i in range(1000):
        db.session.add(Problem(name=f'Binary Tree Tilt {i}', description=TEST_PROBLEM_DESCRIPTION,
                                points=5, difficulty=ProblemDifficultyType(random.randint(0,2))))

    db.session.add(test_contest)
    db.session.commit()

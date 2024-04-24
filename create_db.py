from app import app, db
from models import User, Member
import datetime as dt
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        {'username': 'jdoe', 'email': 'jdoe@umd.edu', 'name': 'John Doe',
         'password': generate_password_hash('jdoepw', method='pbkdf2:sha256'), 'role': 'MEMBER'},
        {'username': 'jsmith', 'email': 'jsmith@umd.edu', 'name': 'Jacob Smith',
         'password': generate_password_hash('jsmithpw', method='pbkdf2:sha256'), 'role': 'BOARD'},
        {'username': 'rblack', 'email': 'rblack@umd.edu', 'name': 'Rachel Black',
         'password': generate_password_hash('rblackpw', method='pbkdf2:sha256'), 'role': 'ALUMNI'}
            ]

    for each_user in users:
        print(f'{each_user["username"]} inserted into User')
        a_user = User(username=each_user["username"], email=each_user["email"], name=each_user["name"],
                      password=each_user["password"], role=each_user["role"])
        db.session.add(a_user)
        db.session.commit()

    members = [
        {'user_id': '1', 'name': 'John Doe', 'grad_date': 'May 2025', 'join_date': 'February 2024',
         'mem_status': 'Active', 'mem_category': 'Member', 'mem_phone': '301-746-3836', 'email': 'jdoe@umd.edu', 'mem_linkedin': 'https://www.linkedin.com/in/john-doe-9339596/'},
        {'user_id': '2', 'mem_id': '7397', 'name': 'Jacob Smith', 'grad_date': 'December 2024', 'join_date': 'February 2023',
         'mem_status': 'Active', 'mem_category': 'Board', 'mem_phone': '301-384-9361', 'email': 'jsmith@umd.edu', 'mem_linkedin': 'https://www.linkedin.com/in/jacob-smith-a34460210/'},
        {'user_id': '3', 'mem_id': '2794', 'name': 'Rachel Black', 'grad_date': 'May 2023', 'join_date': 'September 2021',
         'mem_status': 'Inactive', 'mem_category': 'Alumni', 'mem_phone': '402-384-8172', 'email': 'rblack@umd.edu', 'mem_linkedin': 'https://www.linkedin.com/in/rachel-e-black/'}
         ]
    for each_member in members:
        print(f'{each_member["name"]} inserted into Member')
        a_member = Member(user_id=each_member['user_id'], name=each_member['name'], grad_date=each_member['grad_date'], join_date=each_member['join_date'],
                          mem_status=each_member['mem_status'], mem_category=each_member['mem_category'],
                          mem_phone=each_member['mem_phone'], email=each_member['email'], mem_linkedin=each_member['mem_linkedin'])
        db.session.add(a_member)
        db.session.commit()

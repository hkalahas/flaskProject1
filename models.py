from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = "member"

    mem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    grad_date = db.Column(db.String(100))
    join_date = db.Column(db.String(100))
    mem_status = db.Column(db.String(100))
    mem_category = db.Column(db.String(100))
    mem_phone = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50))
    mem_linkedin = db.Column(db.String(200), unique=True)

    users = db.relationship('User', backref='users')

    def __init__(self, user_id, name, grad_date, join_date, mem_status, mem_category, mem_phone,
                 email, mem_linkedin):
        self.user_id = user_id
        self.name = name
        self.grad_date = grad_date
        self.join_date = join_date
        self.mem_status = mem_status
        self.mem_category = mem_category
        self.mem_phone = mem_phone
        self.email = email
        self.mem_linkedin = mem_linkedin

    def __repr__(self):
        return f"{self.name} (ID: {self.member_id})"


class User(UserMixin, db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(20))

    def __init__(self, username, name, email, password, role='PUBLIC'):
        self.username = username
        self.name=name
        self.email = email
        self.password = password
        self.role = role

    # Function for flask_login manager to provider a user ID to know who is logged in
    def get_id(self):
        return self.user_id

    def __repr__(self):
        return f"{self.name} ({self.username})"

    pass

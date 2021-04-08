from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    role = db.Column(db.String(80))


class Tockens(db.Model):
    id = db.Column('tocken_id', db.Integer, primary_key = True)
    email = db.Column(db.String(100))
    gym = db.Column(db.String(100))
    session = db.Column(db.String(100))
    coupon = db.Column(db.String(100), unique=True)
    date_issue = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(100))
    use_date = db.Column(db.DateTime, nullable=True)
    issue_day = db.Column(db.Date)
    coupon_fst = db.Column(db.Integer)
    service = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    u_name = db.Column(db.String(100))
    stno = db.Column(db.String(100))
    next_day = db.Column(db.Date)
    use_day = db.Column(db.Date)
    

    def __init__(self, email, gym, session, coupon, date_issue, status, use_date, issue_day,coupon_fst,service,branch,u_name,stno,next_day,use_day):

        self.email = email
        self.gym = gym
        self.session = session
        self.coupon = coupon
        self.date_issue = date_issue
        self.status = status
        self.use_date = use_date
        self.issue_day = issue_day
        self.coupon_fst = coupon_fst
        self.service = service
        self.branch = branch
        self.u_name = u_name
        self.stno = stno
        self.next_day = next_day
        self.use_day = use_day
        
        
class Service_providers(db.Model):
    id = db.Column('sp_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    service = db.Column(db.String(100))
    location = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    nssf_branch = db.Column(db.String(100))
    max_morn = db.Column(db.Integer)
    max_noon = db.Column(db.Integer)
    max_eve = db.Column(db.Integer)
    max_num = db.Column(db.Integer)
    unit_cost = db.Column(db.Integer)

class End_users(db.Model):
    id = db.Column('eu_id', db.Integer, primary_key = True)
    stno = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(100))
    company = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    branch = db.Column(db.String(100))

class Staff_users(db.Model):
    id = db.Column('su_id', db.Integer, primary_key = True)
    stno = db.Column(db.String(10), unique=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(80))
    phone = db.Column(db.String(100))
    password = db.Column(db.String(100))




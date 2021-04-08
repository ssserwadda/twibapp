from flask import Blueprint, render_template, redirect, url_for, request, flash, g
from flask_login import login_required, current_user
from flask_user import UserMixin, roles_required
from . import db
from functools import wraps
import _datetime
from datetime import datetime
from .models import Tockens, Service_providers, End_users, User
import sqlite3
import pandas as pd
from pandas import DataFrame
#from sqlalchemy import asc, desc


main = Blueprint('main', __name__)

@main.before_request
def before_request():
    g.user = current_user


@main.route('/')
def index():
    return render_template('index.html')

def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_current_user_role() not in roles:
            flash('Authentication error, please check your details and try again','error')
            return redirect(url_for('auth.login'))
         return f(*args, **kwargs)
      return wrapped
   return wrapper
 
def get_current_user_role():
   return g.user.role

@main.route('/profile')
@login_required
@required_roles('s_provider')
def profile():
    issue_day = _datetime.date.today()
    gym=current_user.name
    tockens1 = sp_tockens(gym,'used',issue_day)
    tockens2 = sp_tockens(gym,'booked',issue_day)
    
    tockens = tockens1[0]

    tokn_used = len(tockens1[0])
    tokn_booked = tokn_used + len(tockens2[0])

    tokn_used_td = len(tockens1[1])
    tokn_booked_td = len(tockens2[1])+tokn_used_td

    #tokn_booked =len(sp_tockens1(gym,'booked')) + tokn_used

    #tokn_used_today = len(tockens)
    #tokn_booked =len(sp_tockens(gym,'booked')) + tokn_used


    return render_template('profile.html', tockens = tockens, tokn_used=tokn_used, tokn_used_td=tokn_used_td, 
                tokn_booked=tokn_booked, tokn_booked_td=tokn_booked_td, name = current_user.name)

@main.route('/staffprofile')
@login_required
@required_roles('staff')
def staffprofile():
    email = current_user.email
    issue_day = _datetime.date.today()
    tockens = staff_tockens(email,issue_day)
    #got_id = tockens[0]
    tockn_count = len(tockens)    
    return render_template('staffprofile.html', name = current_user.name, tockens = tockens, tockn_count=tockn_count)

@main.route('/get_food_tocken')
def get_food_tocken():
    conn = sqlite3.connect('project/db.sqlite')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    selectStatement = "SELECT name FROM service_providers WHERE service = 'food'"
    cursor.execute(selectStatement)
    rows = cursor.fetchall()
    sp_names = list(sum(rows, ()))
    return render_template('get_food_tocken.html', sp_names=sp_names)

@main.route('/get_gym_tocken', methods = ['GET', 'POST'])
def get_gym_tocken():
    conn = sqlite3.connect('project/db.sqlite')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    selectStatement = "SELECT name FROM service_providers WHERE service = 'gym'"
    cursor.execute(selectStatement)
    rows = cursor.fetchall()
    sp_names = list(sum(rows, ()))
    return render_template('get_gym_tocken.html', sp_names=sp_names)

@main.route('/search_by')
def search_by():
    return render_template('search_by.html',tocken_count=0)

@main.route('/show_all_users')
def show_all_users():
    headline ="ALL RECOGNISED USERS"
    allusers = User.query.all()
    return render_template('show_all_users.html',headline=headline, allusers=allusers )


@main.route('/show_all_coupons')
def show_all_coupons():
    headline ="ALL COUPONS"
    tockens = Tockens.query.order_by(Tockens.date_issue.desc()).all()
    return render_template('show_all_coupons.html',headline=headline, tockens=tockens )

@main.route('/show_all_providers')
def show_all_providers():
    sps = Service_providers.query.all()
    return render_template('show_all_providers.html', sps=sps )

@main.route('/show_end_users')
def show_end_users():
    eus = End_users.query.all()
    return render_template('show_end_users.html', eus=eus )

@main.route('/show_booked_coupons')
def show_booked_coupons():
    status1='booked'
    headline ="ALL BOOKED COUPONS"
    tockens = Tockens.query.order_by(Tockens.date_issue.desc()).filter_by(status=status1)
    return render_template('show_all_coupons.html', headline=headline,tockens=tockens)

@main.route('/show_used_coupons')
def show_used_coupons():
    headline ="ALL USED COUPONS"
    tockens = Tockens.query.order_by(Tockens.date_issue.desc()).filter_by(status='used')
    return render_template('show_all_coupons.html', headline=headline, tockens = tockens)


@main.route('/checkin')
@required_roles('Admin')
def checkin():
    #return render_template('profile.html', name=current_user.name)
    return 'checkin'



# import library 
import math, random   
# function to generate OTP 
def generateOTP() :  
    # Declare a digits variable   
    # which stores all digits  
    digits = "0123456789"
    OTP = ""   
   # length of password can be chaged 
   # by changing value in range 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)]   
    return OTP

def search_tocken(coupon=""):
    sql_ = "SELECT * FROM tockens WHERE coupon = :c "
    par_ = { "c": coupon}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def search_stno(stno=""):
    sql_ = "SELECT email FROM end_users WHERE stno = :c "
    par_ = { "c": stno}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def search_name(name=""):
    sql_ = "SELECT * FROM end_users WHERE name = :c "
    par_ = { "c": name}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def search_tocken2(stno="",gym="", issue_day=""):
    sql_ = "SELECT * FROM tockens WHERE stno = :c AND gym = :d AND issue_day = :e "
    par_ = { "c": stno, "d": gym, "e": issue_day}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def maxm_slots(name=""):
    sql_ = "SELECT max_num FROM service_providers WHERE name = :c "
    par_ = { "c": name}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def booked_slots(gym="",session="",issue_day=""):
    sql_ = "SELECT * FROM tockens WHERE gym = :c AND session = :d AND issue_day = :e"
    par_ = { "c": gym, "d": session, "e": issue_day}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return len(records)
    cnn.close() 

def sp_tockens(gym="", status="", issue_day =""):
    sql_ = "SELECT * FROM tockens WHERE gym = :c AND status = :d ORDER BY issue_day DESC;"
    sql2 = "SELECT * FROM tockens WHERE gym = :c AND status = :d AND issue_day=:e"
    par_ = { "c": gym,  "d": status}
    par2 = { "c": gym,  "d": status, "e": issue_day}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur2 = cnn.cursor()
    cur.execute(sql_, par_)
    cur2.execute(sql2, par2)
    records = cur.fetchall()
    records2 = cur2.fetchall()
    return records, records2
    cnn.close()


def staff_tockens(email="", issue_day=""):
    sql_ = "SELECT * FROM tockens WHERE email = :c AND issue_day = :d"
    par_ = { "c": email,  "d": issue_day}
    cnn = sqlite3.connect("project/db.sqlite")
    cur = cnn.cursor()
    cur.execute(sql_, par_)
    records = cur.fetchall()
    return records
    cnn.close()

def sp_summarize(gym="",status=""):
    quer = "SELECT * FROM tockens WHERE gym = :c AND status = :d"
    par_ = { "c": gym, "d": status}
    con = sqlite3.connect("project/db.sqlite")
    cur = con.cursor()
    cur.execute(quer, par_)
    records = cur.fetchall()
    return records
    cnn.close()

@main.route('/daily_food_summary')
def daily_food_summary():
    con = sqlite3.connect("project/db.sqlite")
    quer="SELECT * FROM tockens where status = 'used'"

    df=pd.read_sql(quer,con)
    df['issue_day'] = pd.to_datetime(df['issue_day'], dayfirst = True)
    df['period'] = (df['issue_day'].dt.year)*100+(df['issue_day'].dt.month)
    
    df1 = df[df['service']=='food']
    day_by_food=pd.crosstab(df1.issue_day,df1.gym)
    day_by_food.sort_values(by=['issue_day'], inplace=True, ascending=False)
    all_totals = [day_by_food.to_html(classes='data', header="true")]
    
    headline ="DAILY FOOD COUPONS"
    return render_template('summary.html', all_totals=all_totals, headline=headline)

@main.route('/monthly_food_summary')
def monthly_food_summary():
    con = sqlite3.connect("project/db.sqlite")
    quer="SELECT * FROM tockens where status = 'used'"

    df=pd.read_sql(quer,con)
    df['issue_day'] = pd.to_datetime(df['issue_day'], dayfirst = True)
    df['period'] = (df['issue_day'].dt.year)*100+(df['issue_day'].dt.month)
    
    df1 = df[df['service']=='food']
    month_by_food=pd.crosstab(df1.period,df1.gym)
    month_by_food.sort_values(by=['period'], inplace=True, ascending=False)
    all_totals = [month_by_food.to_html(classes='data', header="true")]

    headline ="MONTHLY FOOD COUPONS"
    return render_template('summary.html', all_totals=all_totals, headline=headline)


@main.route('/daily_gym_summary')
def daily_gym_summary():
    con = sqlite3.connect("project/db.sqlite")
    quer="SELECT * FROM tockens where status = 'used'"

    df=pd.read_sql(quer,con)
    df['issue_day'] = pd.to_datetime(df['issue_day'], dayfirst = True)
    df['period'] = (df['issue_day'].dt.year)*100+(df['issue_day'].dt.month)

    df2 = df[df['service']=='gym']
    day_by_gym=pd.crosstab(df2.issue_day,df2.gym)
    day_by_gym.sort_values(by=['issue_day'], inplace=True, ascending=False)
    all_totals = [day_by_gym.to_html(classes='data', header="true")]

    headline ="DAILY GYM COUPONS"
    return render_template('summary.html', all_totals=all_totals, headline=headline)
 

@main.route('/monthly_gym_summary')
def monthly_gym_summary():
    con = sqlite3.connect("project/db.sqlite")
    quer="SELECT * FROM tockens where status = 'used'"

    df=pd.read_sql(quer,con)
    df['issue_day'] = pd.to_datetime(df['issue_day'], dayfirst = True)
    df['period'] = (df['issue_day'].dt.year)*100+(df['issue_day'].dt.month)
    
    df2 = df[df['service']=='gym']
    month_by_gym=pd.crosstab(df2.period,df2.gym)
    #month_by_gym.sort_values(by=['period'], inplace=True, ascending=False)
    month_by_gym.sort_values(by=['period'], inplace=True, ascending=False)
    all_totals = [month_by_gym.to_html(classes='data', header="true")]

    headline ="MONTHLY GYM COUPONS"
    return render_template('summary.html', all_totals=all_totals, headline=headline)



@main.route('/sp_groupings')
@login_required
@required_roles('s_provider')
def sp_groupings():
    gym= current_user.name

    aa = sp_summarize(gym,'used')
    df = DataFrame (aa, columns=['tocken_id', 'email','gym','session','coupon','date_issue','status','use_date','issue_day','coupon_fst',
                        'service','branch', 'u_name','stno', 'next_day', 'use_day'])
    df2 =df.loc[:, ('session','coupon','issue_day')]

    df3=pd.crosstab(df.issue_day,df.session,values=df.coupon, aggfunc='count', margins=True)
    df4 = df3.sort_values(by='issue_day',ascending=False).fillna(0).astype(int)

    df2['issue_day'] = pd.to_datetime(df2['issue_day'], dayfirst = True)
    df2['Period'] = (df2['issue_day'].dt.year)*100+(df2['issue_day'].dt.month)


    df5=pd.crosstab(df2.Period,df2.session,values=df2.coupon, aggfunc='count', margins=True).fillna(0)
    
    #df6 = df5.sort_values(by='Period',ascending=False).fillna(0)
    by_days = [df4.to_html(classes='data', header="true")]
    by_months = [df5.to_html(classes='data', header="true")]
    

    return render_template('sp_groupings.html', by_days=by_days, by_months=by_months, gym = gym )
    


@main.route('/get_tocken', methods = ['GET', 'POST'])
@login_required
@required_roles('staff')
def get_tocken():

    if request.method == 'POST':
#        if not request.form['gym'] or not request.form['session']:
#            flash('Please enter all the fields', 'error')
#        else:
        coupon1 = generateOTP()
        uniq_coupon = Tockens.query.filter_by(coupon_fst=coupon1).count()
        if uniq_coupon > 0:
            coupon= str(coupon1) + str(uniq_coupon+1)                
        else:
            coupon = coupon1
            
        coupon_fst = coupon1

        date_issue = datetime.now()
        #issue_day = _datetime.date.today()
        status = "booked"
        use_date = datetime.now()
        gym = request.form['gym']
        service = request.form['service']
        session1 = request.form['session']
        #email2 = request.form['email']
        email = current_user.email
        name = current_user.name
        userdetails = search_name(name)
        branch = userdetails[0][6]
        u_name = userdetails[0][2]
        stno = userdetails[0][1]
        next_day = _datetime.date.today() + _datetime.timedelta(days = 1)
        use_day = _datetime.date.today()
        
        only_one = Tockens.query.filter_by(email=email, service=service, issue_day=_datetime.date.today()).count()

        issue_day = _datetime.date.today()

        sesn_slots = booked_slots(gym,session1,issue_day)

        #name = gym
        slot_limit_list = maxm_slots(gym)
        slot_limit = int(slot_limit_list[0][0])

        #validating sessions
        issue_hour = date_issue.hour
        #issue_day = date_issue.day  

        if service != "gym":
            session = session1
            if only_one > 0:
                flash('You have already booked a coupon for this service today. Try tomorrow')
                return redirect(url_for('main.get_gym_tocken'))
            elif sesn_slots >= slot_limit:
                flash('slots for this session are all booked')
                return redirect(url_for('main.get_food_tocken'))
            else:
                tocken = Tockens(email, request.form['gym'],request.form['session'], coupon, date_issue, status, use_date, issue_day,coupon_fst,service,branch,u_name,stno,next_day,use_day )
        
                db.session.add(tocken)
                db.session.commit()
                return redirect(url_for('main.staffprofile'))
            return render_template('get_food_tocken.html')

        else:
            if (issue_hour > 16):
                if(session1 == 'morning'):
                    flash('Its too late to book for a morning session today. Try evening or tomorrow')
                    return redirect(url_for('main.get_gym_tocken'))
                elif(session1 == 'afternoon'):
                    flash('Its too late to book for an afternoon session today. Try evening or tomorrow')
                    return redirect(url_for('main.get_gym_tocken'))
                else:
                    session = session1

            elif (issue_hour > 11):
                if (session1 == 'morning'):
                    flash('Its too late to book for a morning session today. Try afternoon, evening or tomorrow')
                    return redirect(url_for('main.get_gym_tocken'))
                else:
                    session = session1            
            else:
                session = session1

            if only_one > 0:
                flash('You have already booked a coupon for this service today. Try tomorrow')
                return redirect(url_for('main.get_gym_tocken'))
            elif sesn_slots >= slot_limit:
                flash('slots for this session are all booked')
                return redirect(url_for('main.get_gym_tocken'))
            else:
                tocken = Tockens(email, request.form['gym'],request.form['session'], coupon, date_issue, status, use_date, issue_day,coupon_fst,service,branch,u_name,stno,next_day,use_day )
        
                db.session.add(tocken)
                db.session.commit()
                return redirect(url_for('main.staffprofile'))

            return render_template('get_gym_tocken.html')
    return render_template('get_gym_tocken.html')                     






@main.route("/searchdata")
def searchdata():
    return render_template('searchdata.html')    


@main.route("/searchdata2")
def searchdata2():
    return render_template('searchdata2.html') 

@main.route('/search_results', methods=['GET', 'POST'])
@login_required
@required_roles('s_provider')
def search_results():
    coupon = request.form['coupon']
    results = search_tocken(coupon)
    num_tokn = len(results)
    if num_tokn < 1:
        flash("There is no coupon of that kind", 'warning')
        return redirect(url_for('main.searchdata'))
            
    email = current_user.email
    gym = current_user.name
    got_gym = results[0][2]

    if got_gym != gym:
        flash('This coupon is for another service provider')
        return redirect(url_for('main.searchdata'))    

    got_id = results[0][0]
    got_session = results[0][3]
    got_status = results[0][6]
    got_service = results[0][10]
    date_issue = datetime.strptime(results[0][5], '%Y-%m-%d %H:%M:%S.%f')
    issue_day = date_issue.day
    checkin_date = datetime.now()
    checkin_hour = checkin_date.hour
    checkin_day = checkin_date.day
    
   
    if checkin_hour > 16:
        period = 'evening'
    elif checkin_hour > 11:
        period = 'afternoon'
    else:
        period = 'morning'


    if got_status == 'used':
        flash('This coupon is already used')
        return redirect(url_for('main.searchdata'))
    elif issue_day  != checkin_day:
        flash('This coupon is already expired due to date of issue')
        return redirect(url_for('main.searchdata'))        
 
    elif got_service =="gym":
        if period != got_session:
            flash('This coupon is already expired due to session')        
            return redirect(url_for('main.searchdata'))
        return render_template('searchdata.html', results=results, got_id =got_id )    
    else:
        return render_template('searchdata.html', results=results, got_id =got_id )
        
@main.route('/search_results2', methods=['GET', 'POST'])
@login_required
@required_roles('s_provider')
def search_results2():
    stno = request.form['stno']

    #rezult = search_stno(stno)
    #email = rezult[0][4]
    gym = current_user.name

    issue_day = _datetime.date.today()
    
    results = search_tocken2(stno,gym,issue_day)
    num_tokn = len(results)
    if num_tokn < 1:
        flash("There is no valid coupon for this STNO for this sevice provider today ")
        return redirect(url_for('main.searchdata2'))
            
    email = current_user.email
    gym = current_user.name
    got_gym = results[0][2]

    if got_gym != gym:
        flash('This coupon is for another service provider')
        return redirect(url_for('main.searchdata2'))    

    got_id = results[0][0]
    got_session = results[0][3]
    got_status = results[0][6]
    got_service = results[0][10]
    date_issue = datetime.strptime(results[0][5], '%Y-%m-%d %H:%M:%S.%f')
    issue_de = date_issue.day
    checkin_date = datetime.now()
    checkin_hour = checkin_date.hour
    checkin_day = checkin_date.day
    
   
    if checkin_hour > 16:
        period = 'evening'
    elif checkin_hour > 11:
        period = 'afternoon'
    else:
        period = 'morning'


    if got_status == 'used':
        flash('Todays coupon for this STNO is already used')
        return redirect(url_for('main.searchdata2'))
    elif issue_de  != checkin_day:
        flash('This coupon is already expired due to date of issue')
        return redirect(url_for('main.searchdata2'))        
 
    elif got_service =="gym":
        if period != got_session:
            flash('This coupon is already expired due to session')        
            return redirect(url_for('main.searchdata2'))
        return render_template('searchdata2.html', results=results, got_id =got_id )    
    else:
        return render_template('searchdata2.html', results=results, got_id =got_id )

@main.route('/search_by_results', methods=['GET','POST'])
def search_by_results():
    choice = request.form['choice']
    date1 = request.form['date1']
    date2 = request.form['date2']
    search_item = request.form['search_item'].lower()
    
    #datetokns=
    if choice == 'Status':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1).filter_by(status=search_item)
    elif choice == 'Shift':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1).filter_by(session=search_item)
    elif choice == 'Coupon':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1).filter_by(coupon=search_item)
    elif choice == 'Service Provider':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1).filter_by(gym=search_item)
    elif choice == 'Service':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1).filter_by(service=search_item)
    elif choice == 'All':
        tockens = Tockens.query.filter(Tockens.issue_day <= date2).filter(Tockens.issue_day >= date1)
    else:
        tockens = Tockens.query.all()

    tocken_count = tockens.count()

    if tocken_count < 1:
        flash('There is no coupon of that kind')
        return redirect(url_for('main.search_by'))    

 
    return render_template('search_by.html', tockens=tockens, tocken_count=tocken_count, choice=choice, date1=date1, date2=date2, search_item=search_item)

@main.route('/expired')
def expired():
    status1='booked'
    return render_template('show_all_coupons.html', tockens = Tockens.query.filter_by(status=status1))  

@main.route('/check_in/<int:id>', methods=['GET', 'POST'])
def check_in(id):
    tocken = Tockens.query.get_or_404(id)
    if request.method == 'POST':
        tocken.status = request.form['status']
        tocken.use_date = request.form['use_date']

        try:
            db.session.commit()
            flash('This coupon hass been successifully used')
            return redirect(url_for('main.searchdata'))
        except:
            flash('There was a problem updating data')
            

    else:
        tocken.status = "used"
        tocken.use_date = datetime.now()
        tocken.use_day = _datetime.date.today()
        db.session.commit()
        #flash('This coupon has been successifully cashed') 
        return redirect(url_for('main.profile'))

@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    tocken = Tockens.query.get_or_404(id)
    conn = sqlite3.connect('project/db.sqlite')
    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    selectStatement = "SELECT name FROM service_providers WHERE service = 'gym'"
    cursor.execute(selectStatement)
    rows = cursor.fetchall()
    sp_names = list(sum(rows, ()))
      
    if request.method == 'POST':
        tocken.gym = request.form['gym']
        tocken.session = request.form['session']

        date_issue = datetime.now()
        gym = request.form['gym']        
        session1 = request.form['session']        

        issue_day = _datetime.date.today()
        sesn_slots = booked_slots(gym,session1,issue_day)

        #name = gym
        slot_limit_list = maxm_slots(gym)
        slot_limit = int(slot_limit_list[0][0])

        #validating sessions
        issue_hour = date_issue.hour

        if (issue_hour > 16):
            if(session1 == 'morning'):
                flash('Its too late to book for a morning session today. Try evening or tomorrow')
                return render_template('update.html', tocken=tocken, sp_names=sp_names)
            if(session1 == 'afternoon'):
                flash('Its too late to book for an afternoon session today. Try evening or tomorrow')
                return render_template('update.html', tocken=tocken, sp_names=sp_names)

        elif (issue_hour > 11):
            if (session1 == 'morning'):
                flash('Its too late to book for a morning session today. Try afternoon, evening or tomorrow')
                return render_template('update.html', tocken=tocken, sp_names=sp_names)

        if sesn_slots >= slot_limit:
            flash('slots for this session are all booked')
            return render_template('update.html', tocken=tocken, sp_names=sp_names)
        else:                    
            db.session.commit()
            return redirect(url_for('main.staffprofile'))
                   


        try:
            db.session.commit()
            #flash('This coupon hass been successifully used')
            return redirect(url_for('main.staffprofile'))
        except:
            flash('There was a problem updating data')
            

    else:

        #title = "Check in coupon"
        #tocken.session = request.form['session']
        return render_template('update.html', tocken=tocken, sp_names=sp_names)


@main.route('/update2/<int:id>', methods=['GET', 'POST'])
def update2(id):
    tocken = Tockens.query.get_or_404(id)
    conn = sqlite3.connect('project/db.sqlite')
    cursor2 = conn.cursor()
    selectStatement2 = "SELECT name FROM service_providers WHERE service = 'food'"
    cursor2.execute(selectStatement2)
    rows2 = cursor2.fetchall()
    fp_names = list(sum(rows2, ()))
  
    
    if request.method == 'POST':
        tocken.gym = request.form['gym']
        tocken.session = request.form['session']
        #tocken.date_issue = request.form['date_issue']
        date_issue = datetime.now()
        gym = request.form['gym']
        
        session1 = request.form['session']        

        issue_day = _datetime.date.today()
        sesn_slots = booked_slots(gym,session1,issue_day)

        #name = gym
        slot_limit_list = maxm_slots(gym)
        slot_limit = int(slot_limit_list[0][0])

        #validating sessions
        issue_hour = date_issue.hour
           

        if sesn_slots >= slot_limit:
            flash('slots for this session are all booked')
            return render_template('update2.html', tocken=tocken, fp_names=fp_names)
        else:                    
            db.session.commit()
            return redirect(url_for('main.staffprofile'))

    return render_template('update2.html', tocken=tocken, fp_names=fp_names)


@main.route('/update_end_users/<int:id>', methods=['GET', 'POST'])
def update_end_users(id):
    end_user = End_users.query.get_or_404(id)
    if request.method == 'POST':
        end_user.stno = request.form['stno']
        end_user.name = request.form['name']
        end_user.company = request.form['company']
        end_user.email = request.form['email']
        end_user.phone = request.form['phone']
        end_user.branch = request.form['branch']

        try:
            db.session.commit()
            #flash('This coupon hass been successifully used')
            return redirect(url_for('main.show_end_users'))
        except:
            flash('There was a problem updating data')
            

    else:

        return render_template('update_end_users.html', end_user=end_user)
    return render_template('update_end_users.html', end_user=end_user)

@main.route('/delete_end_users/<int:id>')
def delete_end_users(id):
    end_user = End_users.query.get_or_404(id)

    try:
        db.session.delete(end_user)
        db.session.commit()
        return redirect(url_for('main.show_end_users'))
    except:
        return "There was a problem deleting data."

@main.route('/delete_providers/<int:id>')
def delete_providers(id):
    svc_provider = Service_providers.query.get_or_404(id)

    try:
        db.session.delete(svc_provider)
        db.session.commit()
        return redirect(url_for('main.show_all_providers'))
    except:
        return "There was a problem deleting data."

@main.route('/update_providers/<int:id>', methods=['GET', 'POST'])
def update_providers(id):
    svc_provider = Service_providers.query.get_or_404(id)
    if request.method == 'POST':
        svc_provider.name = request.form['name']
        svc_provider.service = request.form['service']
        svc_provider.location = request.form['location']
        svc_provider.email = request.form['email']
        svc_provider.phone = request.form['phone']
        svc_provider.nssf_branch = request.form['nssf_branch']
        svc_provider.max_morn = request.form['max_morn']
        svc_provider.max_noon = request.form['max_noon']
        svc_provider.max_eve = request.form['max_eve']
        svc_provider.max_num = request.form['max_num']
        svc_provider.unit_cost = request.form['unit_cost']

        

        try:
            db.session.commit()
            #flash('This coupon hass been successifully used')
            return redirect(url_for('main.show_all_providers'))
        except:
            flash('There was a problem updating data')
            

    else:

        return render_template('update_providers.html', svc_provider=svc_provider)
    return render_template('update_providers.html', svc_provider=svc_provider)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
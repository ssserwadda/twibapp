from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required, logout_user
from .models import User, End_users, Staff_users, Service_providers
from . import db
import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/staff_signup')
def staff_signup():
    return render_template('staff_signup.html')


@auth.route('/end_users')
def end_users():
    return render_template('register_endusers.html', )
    

@auth.route('/s_providers')
def s_providers():
    return render_template('register_providers.html', )
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/staff_logout')
@login_required
def staff_logout():
    logout_user()
    return redirect(url_for('auth.staff_login'))

@auth.route('/staff_login')
def staff_login():
    return render_template('staff_login.html')


def sp_name(email=""):
    quer = "SELECT name FROM service_providers WHERE email = :c "
    par_ = { "c": email}
    con = sqlite3.connect('project/db.sqlite')
    cur = con.cursor()
    cur.execute(quer, par_)
    records = cur.fetchall()
    return records
    cnn.close()

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    #name = request.form.get('name')
    role = 's_provider'
    #service = request.form.get('service')
    password = request.form.get('password')

    pw1 = request.form.get("password2")
    if not pw1 == password:
        flash('Passwords do not match')
        return redirect(url_for('auth.signup'))

    allowed_mail = Service_providers.query.filter_by(email=email).count()
    if allowed_mail < 1:
        flash('Email address is not authorised for this application')
        return redirect(url_for('auth.signup'))       
   
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    
    p_name = sp_name(email)
    name = p_name[0][0]
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, role=role, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

@auth.route('/register_endusers', methods=['GET', 'POST'])
def register_endusers():
    stno = request.form.get('stno')
    name = request.form.get('name')
    company = request.form.get('company')
    email = request.form.get('email')
    phone = request.form.get('phone')
    branch = request.form.get('branch')

    enduser = End_users.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if enduser: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.end_users'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    end_user = End_users(stno=stno, name=name, company=company, email=email, phone=phone,branch=branch)

    # add the new user to the database
    db.session.add(end_user)
    db.session.commit()

    return redirect(url_for('main.index'))


@auth.route('/register_providers', methods=['GET', 'POST'])
def register_providers():
    name = request.form.get('name')
    service = request.form.get('service')
    location = request.form.get('location')
    email = request.form.get('email')
    phone = request.form.get('phone')
    nssf_branch = request.form.get('nssf_branch')
    max_morn = request.form.get('max_morn')
    max_noon = request.form.get('max_noon')
    max_eve = request.form.get('max_eve')
    max_num = request.form.get('max_num')
    unit_cost = request.form.get('unit_cost')

    s_provider = Service_providers.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if s_provider: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.s_providers'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    serv_provider = Service_providers(name=name, service=service, location=location, email=email,phone=phone,\
                    nssf_branch=nssf_branch,max_morn=max_morn,max_noon=max_noon, max_eve=max_eve, max_num=max_num, unit_cost=unit_cost)

    # add the new user to the database
    db.session.add(serv_provider)
    db.session.commit()

    return redirect(url_for('main.index'))

def user_name(email=""):
    quer = "SELECT name FROM end_users WHERE email = :c "
    par_ = { "c": email}
    con = sqlite3.connect('project/db.sqlite')
    cur = con.cursor()
    cur.execute(quer, par_)
    records = cur.fetchall()
    return records
    cnn.close()



@auth.route('/staff_signup', methods=['POST'])
def staff_signup_post():
    email = request.form.get('email')

    role = 'staff'
    password = request.form.get('password')
    pw1 = request.form.get("password2")
    if not pw1 == password:
        flash('Passwords do not match')
        #return redirect(url_for('auth.staff_signup'))
   
    allowed_mail = End_users.query.filter_by(email=email).count()
    if allowed_mail < 1:
        flash('Email address is not authorised for this application')
        return redirect(url_for('auth.staff_signup'))       
    else:
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.staff_signup'))

        u_name = user_name(email)
        name = u_name[0][0]
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, role=role, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.staff_login'))


@auth.route('/staff_login', methods=['POST'])
def staff_login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.staff_login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.staffprofile'))
  
@auth.route('/register_all_users')
def register_all_users():
    return render_template('register_all_users.html')



@auth.route('/register_users', methods=['GET', 'POST'])
def register_users():
    name = request.form.get('name')
    email = request.form.get('email')
    role = request.form.get('role')
    password = request.form.get('password')

    if role == 'staff':
        allowed_mail = End_users.query.filter_by(email=email).count()
    elif role == 's_provider':
        allowed_mail = Service_providers.query.filter_by(email=email).count()
    else:
        allowed_mail = 1

    if allowed_mail < 1:
        flash('Email address is not authorised for this application')
        return redirect(url_for('auth.register_all_users'))       
    else:
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.register_all_users'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, role=role, password=generate_password_hash(password, method='sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('main.show_all_users'))


@auth.route('/reset_passwords/<int:id>', methods=['GET', 'POST'])
def reset_passwords(id):
    any_user = User.query.get_or_404(id)
    if request.method == 'POST':
        new_password = request.form['password']
        any_user.password = generate_password_hash(new_password, method='sha256')


        try:
            db.session.commit()
            flash('Password reset was successifully done')
            return redirect(url_for('main.show_all_users'))
            #return render_template('reset_passwords.html', any_user=any_user)
        except:
            flash('There was a problem updating data')
            

    else:

        return render_template('reset_passwords.html', any_user=any_user)
    return render_template('reset_passwords.html', any_user=any_user)

@auth.route('/password_change')
@login_required
def password_change():
    #id = current_user.id
    return render_template('change_password.html')




@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':

        password = request.form.get('password')
        password2 = request.form['password2']
        password3 = request.form['password3']

        tru_pword = current_user.password
        email = current_user.email

        user = User.query.filter_by(email=email).first()

        if not check_password_hash(tru_pword,password):
            flash('Old password is wrong')
            return redirect(url_for('auth.password_change'))
        
        if password2 != password3:
            flash('New passwords do not match')
            return redirect(url_for('auth.password_change'))

        user.password = generate_password_hash(password2, method='sha256')

        try:
            db.session.commit()
            flash('Password reset was successifully done')
            if current_user.role == 'staff':
                return redirect(url_for('auth.staff_logout'))
            elif current_user.role == 's_provider':
                return redirect(url_for('auth.logout'))
            return redirect(url_for('main.index'))

            #return render_template('reset_passwords.html', any_user=any_user)
        except:
            flash('There was a problem updating data')
            

    else:

        return render_template('change_password.html')
    return render_template('change_password.html')
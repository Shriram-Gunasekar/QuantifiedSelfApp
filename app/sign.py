from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Account
from . import db
from flask_login import login_user, login_required, logout_user, current_user

sign = Blueprint('sign', __name__,url_defaults=None, root_path=None) #template_folder not specified

@sign.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Gets Variables From Referencing Form ID
    Simple Login Page Here
    Flash is used to display messages to the user
    Login Template Consists of Simple Form
    
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if(authenticate(username, password) == True):
            visitor = Account.query.filter_by(username=username).first()
            flash('Authorization Complete', category='success')
            login_user(visitor, remember=True)
            return redirect(url_for('views.dashboard'))
        
        elif(authenticate(username, password) == False):
            flash('Authorization Failed. Please check your password', category='error')
        
        elif(authenticate(username, password) == None):
            flash('Your Account probably doesn\'t exist, create a new account?', category='error')
        
    return render_template("login.html", user=current_user)


@sign.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('sign.login'))


@sign.route('/create_account', methods=['GET', 'POST'])
def create_account():
    '''
    Receiving Form Input
    '''
    if request.method == 'POST':
        username = request.form.get('username')
        alias = request.form.get('alias')
        original_password = request.form.get('original_password')
        confirmed_password = request.form.get('confirmed_password')
        
        #  Validating The Form Data Below

        if(validate(username,alias,original_password,confirmed_password) == True):
            new_account = Account(username=username,password=original_password, alias=alias)
            db.session.add(new_account)
            db.session.commit()
            login_user(new_account, remember=True)
            flash('Your account has been created', category='success')
            return redirect(url_for('views.dashboard'))
        
        elif(validate(username,alias,original_password,confirmed_password) == False):
            flash('Constraints Not Satisfied or passwords didn\'t match. Try Again', category='error')
        
        elif(validate(username,alias,original_password,confirmed_password) == None):
            flash('Username taken. Please choose another', category='error')

    return render_template("create_account.html", user=current_user)

### Functions to authenticate and validate

def authenticate(username, password):
    visitor = Account.query.filter_by(username=username).first()
    if visitor:
        if visitor.password == password:
            return True
        else:
            return False
    else:
        return None
    
def validate(username, alias, original_password, confirmed_password):
    visitor = Account.query.filter_by(username=username).first()
    if visitor and visitor.username == username:
        return None
    if (original_password != confirmed_password) or len(username)<5 or len(alias)<5 or not(original_password.isalnum()) or len(original_password)<8:
        return False
    else:
        return True
    
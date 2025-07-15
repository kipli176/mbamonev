from flask import render_template, redirect, url_for, request, flash, session
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user
from auth import auth_bp
from models import Pengguna
import bcrypt

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        tahun = request.form['tahun']
        
        user = Pengguna.query.filter_by(username=username, aktif=True).first()
        print(user)
        # if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        if user:
            login_user(user)
            return redirect(url_for('dashboard.index'))
        
        flash('Username atau password salah', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('main.select_year'))
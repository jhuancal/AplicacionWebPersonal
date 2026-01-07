from flask import Blueprint, render_template, request, session, redirect, url_for
from auth.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if AuthService.validate_user(username, password):
            user_data = AuthService.get_user_details(username)
            session['user_data'] = user_data
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template("auth/login.html", error="Invalid Credentials. Access Denied.")
    
    if session.get('user_data'):
        return redirect(url_for('admin.dashboard'))
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        success, message = AuthService.register_user(username, password, email)
        
        if success:
            return render_template("auth/login.html", error="Registration Successful. Please Login.")
        else:
            return render_template("auth/register.html", error=message)
            
    return render_template("auth/register.html")

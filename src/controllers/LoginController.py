from flask import Blueprint, render_template, redirect, url_for

login_bp = Blueprint("login", __name__)

baseDir = 'screens/login/'

@login_bp.route('/')
def login():
    return render_template(baseDir + 'login.html', full_screen=True)
    
@login_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    return render_template(baseDir + 'registro.html', full_screen=True)
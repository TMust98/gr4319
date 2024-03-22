from app import app
from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.forms import LoginForm
import os
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'logo.png')

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html', title='тесты')


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный логин или пароль', 'danger')
            flash(f'{form.username.data} ///// {generate_password_hash(form.password.data)}')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        flash('Успешный вход', 'success')
        return redirect(next_page)

    return render_template('login.html', title = 'Вход', form = form)


@app.route('/lk', methods=['GET','POST'])
@login_required
def lk():
    return render_template('lk.html', title='Личный кабинет')


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'warning')
    return redirect('index')

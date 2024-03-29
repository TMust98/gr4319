from app import app, db
from flask import render_template, flash, redirect, url_for, send_from_directory, request, abort
from app.forms import LoginForm, RegisterForm
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
    redirect('500.html')
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


@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash('Вы уже зарегистрированный пользователь! Для регистрации нового аккаунта выйдите из системы.', 'warning')
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Успешная регистрация! Теперь можно войти. Ваш ID {user.id}','success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Регистрация')



@app.route('/lk', methods=['GET','POST'])
@login_required
def lk():
    if current_user.is_anonymous:
        abort(403)
    return render_template('lk.html', title='Личный кабинет')


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'warning')
    return redirect('index')


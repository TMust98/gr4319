from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm

@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
    return render_template('index.html', title='тесты')


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Вход пользователя {form.username.data} с паролем {form.password.data}. Запомнить: {form.remember_me.data}', 'success')
        return redirect(url_for('login'))

    return render_template('login.html', title = 'Вход', form = form)

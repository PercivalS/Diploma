from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import db, app
from app.forms import LoginForm, RegistrationForm, EditProfileForm, CardForm, OperationForm, ResetPasswordRequestForm, \
    ResetPasswordForm, TableCardsForm, TableOperationsForm
from app.models import User, Card, Operation
from app.email import send_password_reset_email
from prettytable import PrettyTable, ALL


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CardForm()
    if form.validate_on_submit():
        score = Card(number=form.card.data, user_id=current_user.id,
                     about=form.about.data, type=form.type.data,
                     money=form.money.data, time_end=form.time_end.data)
        if Card.query.filter_by(number=score.number).first():
            flash('Your number is not correct!')
        else:
            db.session.add(score)
            flash('Your number is correct!')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("index.html", title='New card', form=form)


@app.route('/operation', methods=['GET', 'POST'])
@login_required
def operation():
    form = OperationForm()
    if form.validate_on_submit():
        operation = Operation(user_id=current_user.id, type=form.type.data, time=form.time.data, money=form.money.data,
                              card_number = form.card.data)
        db.session.add(operation)
        flash('Your number is correct!')
        db.session.commit()
        return redirect(url_for('operation'))
    return render_template("index.html", title='New operation', form=form)


@app.route('/diploma', methods=['GET'])
def diploma():
    return render_template("diploma.html", title='New operation')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, date_of_birth=form.date_of_birth.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user')
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    scores = current_user.scores.paginate(page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', page=scores.next_num) if scores.has_next else None
    prev_url = url_for('user', page=scores.prev_num) if scores.has_prev else None
    return render_template('user.html', user=current_user, scores=scores.items, next_url=next_url, prev_url=prev_url)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if current_user.check_password(form.password.data):
            current_user.set_password(form.password2.data)
            flash('Your changes have been saved.')
        db.session.commit()
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('edit_profile.html', form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/table_cards', methods=['GET', 'POST'])
@login_required
def table_scores():
    form = TableCardsForm()
    return render_template("table.html", form=form, table=table(Card, form.Radio.data, form.Reverse.data))


@app.route('/table_operations', methods=['GET', 'POST'])
@login_required
def table_operations():
    form = TableOperationsForm()
    return render_template("table.html", form=form, table=table(Operation, form.Radio.data, form.Reverse.data))


def table(TName, data, reverse):
    line_1 = []
    line_2 = []
    line_3 = []
    line_4 = []
    line_5 = []
    ggg = TName.query.filter_by(user_id=current_user.id).all()
    for a in ggg:
        if TName.__name__=='Card':
            line_1.append(a.number)
            line_2.append(a.type)
            line_3.append(a.money)
            line_4.append(a.time_end)
            line_5.append(a.about)
        else:
            line_1.append(a.type)
            line_2.append(a.time)
            line_3.append(a.money)
            line_4.append(a.card_number)
            line_5.append(a.about)
    if TName.__name__=='Card':
        names = ['NUMBER','TYPE','MONEY','TIME OF END','ABOUT']
    else:
        names = ['TYPE', 'TIME', 'MONEY', 'CARD NUMBER', 'ABOUT']
    table = PrettyTable([names[0], names[1], names[2], names[3], names[4]], border=True, hrules=ALL, align='l',
                        format=True, padding_width=1)
    for a in range(0, len(line_1)):
        table.add_row([line_1[a], line_2[a], line_3[a], line_4[a], line_5[a]])
    table.sortby = data
    table.reversesort = reverse
    return(table.get_html_string())

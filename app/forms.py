from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, SelectField, DateTimeField, IntegerField, BooleanField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange, Length, optional
from app.models import User
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    date_of_birth = DateField('Date of birth in format d.m.y', validators=[DataRequired()], format='%d.%m.%Y')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email adress.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Old password', validators=[DataRequired()])
    password2 = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change')


class CardForm(FlaskForm):
    card = IntegerField('Number of card', validators=[DataRequired(), NumberRange(min=1000000000000000, max=9999999999999999)])
    about = StringField('Notes', validators=[DataRequired(), Length(min=0, max=50)])
    type = SelectField('Type', validators=[DataRequired()], choices=[('Credit', 'Credit'), ('Deposit', 'Deposit'), ('Savings', 'Savings')])
    money = IntegerField('Money', validators=[DataRequired(), NumberRange(min=-10000, max=10000)])
    time_end = DateField('Date of end in format d.m.y', validators=[DataRequired()], format='%d.%m.%Y')
    submit = SubmitField('New card')


class OperationForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[('withdrawal', 'withdrawal'), ('Deposit', 'Deposit'), ('refill', 'refill')])
    time = DateTimeField('Time in format d.m.y hh:mm', validators=[DataRequired()], format='%d.%m.%Y %H:%M', default=datetime.now())
    money = IntegerField('Money', validators=[DataRequired(), NumberRange(min=-100000, max=100000)])
    card = StringField('Card', validators=[DataRequired(), Length(min=0, max=25)])
    submit = SubmitField('New operation')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of birth', validators=[DataRequired()], format='%d.%m.%Y')
    submit = SubmitField('Request password reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request password reset')


class TableCardsForm(FlaskForm):
    Radio = RadioField(default='NUMBER', choices=[('NUMBER', 'NUMBER', ), ('TYPE', 'TYPE'), ('MONEY', 'MONEY'), ('TIME OF END', 'TIME OF END')])
    Reverse = BooleanField('Reverse', validators=[optional()])
    submit = SubmitField('Reset')


class TableOperationsForm(FlaskForm):
    Radio = RadioField(default='TIME', choices=[('TIME', 'TIME')
        , ('TYPE', 'TYPE', ), ('MONEY', 'MONEY'), ('CARD NUMBER', 'CARD NUMBER')])
    Reverse = BooleanField('Reverse', validators=[optional()])
    submit = SubmitField('Reset')

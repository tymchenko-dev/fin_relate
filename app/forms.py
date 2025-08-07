from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange, Length
from datetime import date

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=80, message="Username must be between 3 and 80 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords don't match")
    ])

class TransactionForm(FlaskForm):
    """Transaction form"""
    amount = FloatField('Amount', validators=[
        DataRequired(message="Please enter an amount"), 
        NumberRange(min=0.01, message="Amount must be greater than 0")
    ])
    description = StringField('Description', validators=[
        Length(max=200, message="Description must not exceed 200 characters")
    ])
    transaction_type = SelectField('Transaction Type', choices=[
        ('expense', 'Expense'),
        ('income', 'Income')
    ], validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    date = DateField('Date', default=date.today, validators=[DataRequired()])

class CategoryForm(FlaskForm):
    """Category form"""
    name = StringField('Name', validators=[
        DataRequired(), 
        Length(min=2, max=100, message="Name must be between 2 and 100 characters")
    ])
    description = TextAreaField('Description', validators=[
        Length(max=500, message="Description must not exceed 500 characters")
    ])
    color = StringField('Color', validators=[
        Length(min=7, max=7, message="Color must be in #RRGGBB format")
    ], default='#007bff')

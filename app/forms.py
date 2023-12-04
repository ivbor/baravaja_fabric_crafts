from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, DateTimeField, \
    PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

from .models import Good, Order, User


class LoginForm(FlaskForm):
    username = StringField('Email:')
    password = PasswordField('Password:')
    submit = SubmitField('Log in')
    id = 'login-form'


class RegisterForm(FlaskForm):
    username = StringField('Email:')
    password = PasswordField('Password:')
    repeat_password = PasswordField('Repeat password:')
    submit = SubmitField('Register')
    id = 'register-form'


class EditUserForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    email = StringField('Email',
                        validators=[DataRequired()])
    street_name = StringField('Street Name', validators=[Optional()])
    street_number = IntegerField('Street Number', validators=[Optional()])
    apt_number = IntegerField('Apt. Number', validators=[Optional()])
    city = StringField('City', validators=[Optional()])
    region = StringField('Region', validators=[Optional()])
    post_index = StringField('Post Index', validators=[Optional()])
    phone_num = StringField('Phone Number', validators=[Optional()])
    rec_id = IntegerField('Recommendations Id', validators=[Optional()])
    orders_ids = StringField('Orders Ids', validators=[Optional()])
    is_admin = BooleanField('Admin', validators=[Optional()])
    password = StringField('Password', validators=[DataRequired()])


class EditGoodForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    photos = StringField('Photos', validators=[DataRequired()])


class EditOrderForm(FlaskForm):
    id = IntegerField('ID', validators=[DataRequired()])
    user_id = IntegerField('UserID', validators=[DataRequired()])
    summ = FloatField('Sum', validators=[DataRequired()])
    contents = StringField('Contents', validators=[DataRequired()])
    datetime = DateTimeField('Creation Datetime', validators=[DataRequired()])


class DeleteForm(FlaskForm):
    pass


obj_map = {'user': (EditUserForm, User),
           'order': (EditOrderForm, Order), 'good': (EditGoodForm, Good)}

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField, PasswordField, SelectMultipleField
from wtforms.fields.html5 import DateField, EmailField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Optional, InputRequired, Email
from models import user
from datetime import datetime


class ItemForm(FlaskForm):
    """
    A class that inherits from the flask form class and allows easy adding creation of forms by simply specifying:
    1. The type of field
    2. The parameters for that field which are the label and validators if any
    """
    data_source = [(1, "Electronics"), (2, "Decor"), (3, "Stationery"), (4, "Tools & Applianc"), (5, "Sports"),
                   (6, "Book"), (7, "Collectibles"), (8, "Game"), (9, "Movie"), (10, "Music"), (11, "Programming"), (12, "Outdoors")]

    item_name = StringField("Item Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    tags = SelectMultipleField("Choose the most appropriate tags:", choices=data_source, coerce=int, validators=[Optional()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 128)])  # Should the min length be >1?
    password = PasswordField("Password:", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class SignUpForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired(), Length(1, 128)])
    username = StringField("Username: ", validators=[DataRequired(), Length(1, 128),
                                                     Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                            'Usernames must only have letters numbers, dots or '
                                                            'underscores')])
    email = EmailField("Email Address: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password:", validators=[DataRequired(), EqualTo('confirm_password',
                                                                              message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password:", validators=[DataRequired()])
    phonenumber = StringField("Phone Number (optional): ", validators=[Optional(), Length(8)])
    submit = SubmitField("Sign Up")

    def validate_username(self, field):
        """
        FlaskWTF automatically uses this validator on the form field that has the same name as the word after validate_
        in the function name.
        :param field:
        :return:
        """
        if user.get_user_by_username(field.data):
            raise ValidationError("Username already in use")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password:", validators=[DataRequired()])
    new_password = PasswordField("New Password:", validators=[DataRequired(), EqualTo('confirm_password',
                                                                              message='Passwords must match.')])
    confirm_password = PasswordField("Confirm Password:", validators=[DataRequired()])
    submit = SubmitField("Change Password")


class BidForm(FlaskForm):
    price = DecimalField('Price: ', validators=[DataRequired()])
    submit = SubmitField("Add your bid")


class GenerateLoanForm(FlaskForm):
    return_date = DateField('Expected date of return: ', format='%Y-%m-%d',
                                     validators=[InputRequired()], default='')
    return_loc = StringField("Return location: ", validators=[DataRequired(), Length(1, 512)])
    pickup_loc = StringField("Pickup location: ", validators=[DataRequired(), Length(1, 512)])
    submit = SubmitField("Generate Loan!")

    def validate_return_date(self, field):
        print(field.data)
        dt = datetime.strptime(str(field.data), '%Y-%m-%d')
        if dt < datetime.now():
            raise ValidationError("That date has passed")

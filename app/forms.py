from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField, PasswordField, FileField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Optional, InputRequired
from models import user
from datetime import datetime


class ItemForm(FlaskForm):
    """
    A class that inherits from the flask form class and allows easy adding creation of forms by simply specifying:
    1. The type of field
    2. The parameters for that field which are the label and validators if any
    """
    item_name = StringField("Item Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    image = FileField("Item Image: ", validators=[Optional()])
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

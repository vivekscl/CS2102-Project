from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, ValidationError, Optional
from models import user


class ItemForm(FlaskForm):
    """
    A class that inherits from the flask form class and allows easy adding creation of forms by simply specifying:
    1. The type of field
    2. The parameters for that field which are the label and validators if any
    """
    item_name = StringField("Item Name: ", validators=[DataRequired()])
    description = StringField("Description: ", validators=[DataRequired()])
    price = DecimalField('Price: ', validators=[DataRequired()])
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


class SearchForm(FlaskForm):
    search = StringField("", validators=[DataRequired()])

class SearchByOwnerForm(FlaskForm):
    search = StringField("", validators=[DataRequired()])



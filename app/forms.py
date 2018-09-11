from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired


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

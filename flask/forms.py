# import libraries
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms_components import DateRange
from datetime import datetime, timedelta, date

today = datetime.now()
while today.weekday() > 4:
    today -= timedelta(1)
while today.weekday() < 4:
    today += timedelta(1)
last_date = today + timedelta(30)
today = today.strftime("%Y-%m-%d")
last_date = last_date.strftime("%Y-%m-%d")

# create a user signup / registration form
class RegistrationForm(FlaskForm):
    # required information for creating an account
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=1, max=16, message="Name length must be greater than 1 characters."),
    ])

    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Input must be a valid email.")
    ])

    phone = StringField("Phone Number", validators=[
        DataRequired(),
        Length(10, 10, message="Phone number length must be 10 digits."),
        Regexp(regex="^ *[0-9][0-9 ]*$", message="Phone number must only be numbers, obviously...")
    ])

    university = SelectField("University",
        choices=[("UT Dallas", "UT Dallas")],
        validators=[DataRequired()
    ])

    budget = SelectField("Budget",
        choices=[("100", "$100"), ("200", "$200"), ("300", "$300"), ("400", "$400"), ("500", "$500"), ("600", "$600"), ("700", "$700"), ("800", "$800"), ("900", "$900"), ("1000", "$1000")],
        validators=[DataRequired()
    ])

    weekend = DateField("Weekend Available", format='%Y-%m-%d', validators=[
        DateRange(min=date.today(), max=date.today() + timedelta(30), message="Pick a day between today and 30 days from now."),
        DataRequired()])

    interests = StringField("Interests (space seperated)", validators=[
        Length(min=0, max=500, message="Length too long! Max is 500 characters."),
    ])

    # submit field
    submit = SubmitField("Submit")
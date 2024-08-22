from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Optional

class SignUpForm(FlaskForm):
    """Form for registering"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)])
    image_url = StringField("Image_URL(Profile-pic)", validators=[Optional()])

class LoginForm(FlaskForm):
    """Form for logging back in"""
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=15)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=20)])

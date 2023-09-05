from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, Optional

class UserRegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=5, max=20, message="username must be between 5 and 20 characters long")])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email(), Length(max=50, message="email must be within 50 characters long")])
    first_name = StringField("First Name",validators=[Length(max=30, message="must be maximum of 30 characters long"), Optional()])
    last_name = StringField("Last Name",validators=[Length(max=30, message="must be maximum of 30 characters long"), Optional()])
    
class UserLoginForm(FlaskForm):
    username = StringField("Username",validators=[Length(max=20, message="must be maximum of 20 characters long"), InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    
class FeedbackForm(FlaskForm):
    title = StringField("Title",validators=[InputRequired()])
    content = TextAreaField("Content",validators=[InputRequired()])
from wtforms import Form, StringField, validators, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('Email', validators=[Email(), DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    
class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    
class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
    pass
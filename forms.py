from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length,Email, NumberRange

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Sign Up')



class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    author = StringField('Author', validators=[DataRequired(), Length(min=2, max=50)])
    isbn = IntegerField('ISBN', validators=[DataRequired()])
    length = IntegerField('Length',validators=[DataRequired(),NumberRange(min=10,max=10000)])
    format = SelectField(
        'Format', 
        choices=[('hardcover', 'Hardcover'), ('paperback', 'Paperback')],
        validators=[DataRequired()]
    )
    submit = SubmitField('Submit')
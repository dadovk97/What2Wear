from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from w2w.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField ('Email',
                         validators=[DataRequired(), Email()])
    password = PasswordField ('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField ('Confirm Password',   
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, choose a different one')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')


class LoginForm(FlaskForm):
    email = StringField ('Email',
                         validators=[DataRequired(), Email()])
    password = PasswordField ('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')   

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                             validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField ('Email',
                         validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, choose a different one')
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')


class PostForm(FlaskForm):
    item = SelectField('item', choices = [('T-shirt'), ('Pants'), ('Jacket'), ('Footwear')])
    color = SelectField('color', choices = [('Black'), ('Gray'), ('White'),('Yellow'),
     ('Orange'), ('Red'),('Pink'), ('Purple'), ('Blue'),('Green'), ('Brown')])
    occasion = SelectField('occasion', choices = [('Casual'), ('Sport'), ('Formal')])
    waterproof = BooleanField('waterproof')
    winter = BooleanField('winter')
    spring = BooleanField('spring')
    summer = BooleanField('summer')
    autumn = BooleanField('autumn')
    public_closet = BooleanField('public_closet')
    image = FileField('Upload Picture', validators = [FileAllowed(['jpg', 'png'])])
    #img_clothes = FileField('Upload Picture', validators = [FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save')


#prognoza

class WeatherForm(FlaskForm):
    city = StringField('city', validators=[DataRequired()])
    public_rec = BooleanField('public_rec')
    submit = SubmitField('Find')
   

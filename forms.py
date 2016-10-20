from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email


class Register(FlaskForm):

    id = StringField('ID',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Submit')

class Login(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class PwdResetRequest(FlaskForm):
    email = StringField('Email')
    submit = SubmitField('Submit')

class PwdReset(FlaskForm):
    username = StringField('Email')
    newpwd = PasswordField('Password')
    submit = SubmitField('Submit')

#class Blogs(FlaskForm):
#    title = StringField('Title')
#    blog = StringField('Blog')
#    submit = SubmitField('Submit')

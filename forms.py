from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email


class Register(Form):

    id = StringField('ID',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Submit')

class Login(Form):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class PwdResetRequest(Form):
    email = StringField('Email')
    submit = SubmitField('Submit')

class PwdReset(Form):
    username = StringField('Email')
    newpwd = PasswordField('Password')
    submit = SubmitField('Submit')

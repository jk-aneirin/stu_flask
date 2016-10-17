from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email


class EmailPasswordForm(Form):

    id = StringField('ID',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField('Submit')

class TForm(Form):
    name = StringField('Name')
    submit = SubmitField('Submit')

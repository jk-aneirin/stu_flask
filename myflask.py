from flask import Flask,render_template,redirect,url_for,flash
from forms import EmailPasswordForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager,Server

app=Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
manager = Manager(app)
manager.add_command("runserver",Server(host="0.0.0.0",port=5000))
db=SQLAlchemy(app)

class Userinfo(db.Model):
    __tablename__='userinfo'
    id = db.Column(db.Integer, primary_key=True)
    email=db.Column(db.Integer)
    password=db.Column(db.String(128),unique=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():
        #add authenticate step
        if app.config['EMAIL']==form.email.data and\
                app.config['PASSWORD']==form.password.data:
            return render_template('loginok.html')
        else:
            flash('EMAIL or PASSWORD wrong')
    return render_template('login.html',form=form)

if __name__ == '__main__':
    db.create_all()
    manager.run()

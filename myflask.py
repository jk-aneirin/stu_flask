from flask import Flask,render_template,redirect,url_for,flash
from forms import Register,Login
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
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128),unique = True)

    def __repr__(self):
        return '<Userinfo %r>' % self.username

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    loginform = Login()
    if loginform.validate_on_submit():
        user = Userinfo.query.filter_by(username=loginform.username.data).first()
        if user is None:
            return redirect(url_for('register'))
        else:
            return redirect(url_for('loginok'))
    return render_template('login.html',form=loginform)

@app.route('/register',methods=['GET','POST'])
def register():
    registerform = Register()
    if registerform.validate_on_submit():
        user = Userinfo.query.filter_by(username=registerform.username.data).first()
        if user is None:
            flash('Hello the New!')

            user=Userinfo(id=registerform.id.data,username=registerform.username.data,\
                    password=registerform.password.data,email=registerform.email.data)
            db.session.add(user)
        else:
            return redirect(url_for('registered'))
    return render_template('register.html',form=registerform)

@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/loginok')
def loginok():
    return render_template('loginok.html')

if __name__ == '__main__':
    db.create_all()
    manager.run()

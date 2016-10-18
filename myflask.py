from flask import Flask,render_template,redirect,url_for,flash
from forms import Register,Login,PwdResetRequest,PwdReset
from utils.smail import SendMail
from itsdangerous import URLSafeTimedSerializer
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from flask_script import Manager,Server
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)
manager = Manager(app)
manager.add_command("runserver",Server(host="0.0.0.0",port=5000))
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

class Userinfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128),unique = True)

    @hybrid_property
    def pwd(self):
        return self.password

    @pwd.setter
    def _set_password(self,plaintext):
        self.password = bcrypt.generate_password_hash(plaintext)

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
                    pwd=registerform.password.data,email=registerform.email.data)
            db.session.add(user)
        else:
            return redirect(url_for('registered'))
    return render_template('register.html',form = registerform)

@app.route('/pwdresetreq',methods = ['GET','POST'])
def pwdresetreq():
    form = PwdResetRequest()
    if form.validate_on_submit():
        user = Userinfo.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Email is None in DB')
            return redirect(url_for('index'))
        else:
            token = ts.dumps(form.email.data,salt='email-confirm-key')
            confirm_url = url_for('confirm_email',token = token,_external = True)
            html = render_template('activate.html',confirm_url=confirm_url)
            SendMail().sendm(form.email.data,confirm_url)
            flash('Email has been sended,please checkout your mailbox')
    return render_template('pwdresetreq.html',form = form)

@app.route('/pwdreset',methods = ['GET','POST'])
def pwdreset():
    form = PwdReset()
    if form.validate_on_submit():
        user = Userinfo.query.filter_by(username = form.username.data).first()
        if user is None:
            flash('username is None in DB')
        else:
            user.password = form.newpwd.data
            db.session.add(user)
            flash('update password successfully')
    return render_template('pwdreset.html',form = form)

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token,salt="email-confirm-key")
    except:
        abort(404)
    user = ts.loads(token, salt="email-confirm-key", max_age=86400)
    return redirect(url_for('pwdreset'))

@app.route('/registered')
def registered():
    return render_template('registered.html')

@app.route('/loginok')
def loginok():
    return render_template('loginok.html')

if __name__ == '__main__':
    db.create_all()
    manager.run()

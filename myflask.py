from flask import Flask,render_template,redirect,url_for,flash
from forms import EmailPasswordForm
from flask_bootstrap import Bootstrap

app=Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)

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


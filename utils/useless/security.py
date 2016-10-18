from itsdangerous import URLSafeTimedSerializer
from stu_flask.myflask import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

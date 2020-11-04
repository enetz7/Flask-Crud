
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model.user import User
from flask import current_app, render_template, request


@current_app.route(rule='/login',endpoint="bla")
def login():
    return render_template('login.html')

#@current_app.route(rule='/index',endpoint='ble')
def index2():
    return 'index'
current_app.add_url_rule(rule='/index', endpoint='ble', view_func=index2)

@current_app.route(rule='/logout',endpoint='bli')
def logout():
    return 'logout'
@current_app.route(rule='/login', methods=['GET', 'POST'],endpoint='blo')
def login_post():
        usernameForm=request.form.get("username")
        passwordForm=request.form.get("password") 
        session = sessionmaker(bind=create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI')))
        s = session()
        query = s.query(User).filter(User.username==usernameForm)
        result = query.first()
        if(result and result.check_password(passwordForm)):
            return "ole"
        else:
            return "no ole"
        return render_template('login.html')
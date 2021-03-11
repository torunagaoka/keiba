import re
import os

from flask import (
    Blueprint, abort, request, render_template,
    redirect,url_for, flash
)
from flask_login import (
    login_user, login_required, 
    logout_user, current_user
)

from flaskr.models import User, Horse
from flaskr.forms import (RegisteForm, LoginForm, HorseRegist, 
                          HorseDeleteForm, HorseUpdateForm, ForgetPassword
)
from flaskr import db



bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/welcome')
@login_required
def welcome():
    userid = User.return_userid(str(current_user))
    horses = Horse.display_horse(userid)
    delete = HorseDeleteForm(request.form)
    return render_template('welcome.html', horses=horses, delete=delete)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')

@bp.route('/registr', methods=['GET', 'POST'])
def registr():
    form = RegisteForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            userid = form.userid.data,
            password = form.password.data,
        )
        user.add_user()
        return render_template('home.html')
    return render_template('registr.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_userid(form.userid.data)
        if user and user.validate_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next') # 次のURL
            if not next:
                next = url_for('app.welcome')
            return redirect(next)
    return render_template('login.html', form=form)

@bp.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = ForgetPassword(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_userid(form.userid.data)
        if User.conformity_password(user, form.last_password.data):
            User.change_password(user, form.new_password.data)
            return render_template('match.html')
        else:
             return render_template('mismatch.html')
    return render_template('forget_password.html', form=form)


@bp.route('/horse_regist', methods=['GET', 'POST'])
def horse_regist():
    form = HorseRegist(request.form)
    user = User.return_userid(str(current_user))
    
    if request.method == 'POST' and form.validate():
        regist = Horse(
            userid = user,
            horsename = form.horsename.data,
            comment = form.comment.data
        )
        
        regist.add_horse()
        return redirect(url_for('app.welcome'))
    return render_template('horse_regist.html', form=form)

@bp.route('/horse_update/<int:id>', methods=['GET', 'POST'])
def horse_update(id):
    form = HorseUpdateForm(request.form)
    userid = User.return_userid(str(current_user))
    comment = Horse.search_comment(id)
    horsename = Horse.search_horsename(id)
    if request.method == 'POST' and form.validate():
        horsename = form.horsename.data
        comment = form.comment.data
        Horse.horse_update_by_id(id, userid, horsename, comment)
        return redirect(url_for('app.welcome'))
    return render_template('update.html', form=form, horsename=horsename, comment=comment)


@bp.route('/horse_delete', methods=['GET', 'POST'])
def horse_delete():
    form = HorseDeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        id = form.id.data
        Horse.delete_horse(id)
        return redirect(url_for('app.welcome'))
    return redirect(url_for('app.welcome'))


@bp.route('search', methods=['GET', 'POST'])
def search():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    dir = os.path.join(base_dir, 'static/csv/whether_to_run.csv')
    userid = User.return_userid(str(current_user))
    results = Horse.horse_search(dir, userid)
    return render_template('result.html', results=results)

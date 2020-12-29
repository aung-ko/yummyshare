from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, login_user, logout_user

from yummyshare.db import db, User
from .forms import RegistrationForm, LoginForm


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register/', methods=['GET', 'POST'])
def register():
    """
    User registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        # add user to the database
        db.session.add(user)
        db.session.commit()

        # log employee in
        login_user(user)

        # redirect to the login page
        return redirect(url_for('recipe.index'))

    return render_template('auth/register.html', form=form)


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    """
    User login.
    """
    form = LoginForm()

    if form.validate_on_submit():
        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            # log user in
            login_user(user)

            # redirect to the home page
            return redirect(url_for('recipe.index'))
        # when login details are incorrect
        else:
            flash('Invalid username or password.')

    # load login template
    return render_template('auth/login.html', form=form)


@bp.route('/logout/')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()

    # redirect to the login page
    return redirect(url_for('auth.login'))

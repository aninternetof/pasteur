from flask import Blueprint, request, redirect, url_for
from flask.ext.login import login_user, logout_user

from pasteur.extensions import cache, socketio
from pasteur.forms import LoginForm
from pasteur.models import User

main = Blueprint('main', __name__)


@main.route('/api/v1')
@cache.cached(timeout=1000)
def home():
    return "Pasteur API root."


@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        return redirect(request.args.get("next") or url_for(".home"))

    return "Login success."


@main.route("/logout")
def logout():
    logout_user()

    return "Logout success."

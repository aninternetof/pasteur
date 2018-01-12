from flask import Blueprint, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user

from pasteur.extensions import cache, thermostat
from pasteur.forms import LoginForm
from pasteur.models import User

main = Blueprint('main', __name__)


@main.route('/api/v1')
@cache.cached(timeout=1000)
def home():
    return "Pasteur API root V1."


@main.route('/api/v1/target-tempf', methods=["GET", "POST"])
def target_tempf():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['target_tempf'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_tempf']})


@main.route('/api/v1/period', methods=["GET", "POST"])
def target_temp():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['period'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['period']})


@main.route('/api/v1/target-degf-sec', methods=["GET", "POST"])
def target_temp():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['target_degf_sec'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_degf_sec']})


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

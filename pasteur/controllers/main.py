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


@main.route('/api/v1/target-tempc', methods=["GET", "POST"])
def target_tempc():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['target_tempc'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_tempc']})


@main.route('/api/v1/period', methods=["GET", "POST"])
def period():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['period'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['period']})


@main.route('/api/v1/target-degc-sec', methods=["GET", "POST"])
def target_degc_sec():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['target_degc_sec'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_degc_sec']})


@main.route('/api/v1/bottom-margin-degc', methods=["GET", "POST"])
def bottom_margin_degc():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['bottom_margin_degc'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['bottom_margin_degc']})


@main.route('/api/v1/top-margin-degc', methods=["GET", "POST"])
def top_margin_degc():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['top_margin_degc'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['top_margin_degc']})


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

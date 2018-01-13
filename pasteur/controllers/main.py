import os
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user

from pasteur.extensions import cache, thermostat
from pasteur.forms import LoginForm
from pasteur.models import db, User, Run

main = Blueprint('main', __name__)


@main.route('/api/v1')
@cache.cached(timeout=1000)
def home():
    return "Pasteur API root V1."

@main.route('/api/v1/run', methods=["GET","POST"])
def run_view():
    if request.method == 'GET':
        return "Not implemented yet", 501
    if request.method == 'POST':
        name = request.get_json()['name']
        log_file_path = os.path.expanduser('~/Desktop/{}_name'
                                           .format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), name))
        run = Run()
        run.name = name
        run.log_file_path = log_file_path
        db.session.add(run)
        db.session.commit()
        thermostat.attributes['name'] = name
        thermostat.attributes['log_file_path'] = log_file_path
        return "Created run {}".format(name)


@main.route('/api/v1/enabled', methods=["GET", "POST"])
def enabled_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        thermostat.attributes['enabled'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['enabled']})


@main.route('/api/v1/target-temp-degc', methods=["GET", "POST"])
def target_tempc_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        try:
            thermostat.attributes['target_temp_degc'] = float(value)
        except ValueError:
            return "Invalid value", 400
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_temp_degc']})


@main.route('/api/v1/period_s', methods=["GET", "POST"])
def period_s_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        try:
            thermostat.attributes['period_s'] = float(value)
        except ValueError:
            return "Invalid value", 400
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['period_s']})


@main.route('/api/v1/target-degc-minutes', methods=["GET", "POST"])
def target_degc_minutes_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        try:
            thermostat.attributes['target_degc_minutes'] = float(value)
        except ValueError:
            return "Invalid value", 400
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['target_degc_minutes']})


@main.route('/api/v1/bottom-margin-degc', methods=["GET", "POST"])
def bottom_margin_degc_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        try:
            thermostat.attributes['bottom_margin_degc'] = float(value)
        except ValueError:
            return "Invalid value", 400
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['bottom_margin_degc']})


@main.route('/api/v1/top-margin-degc', methods=["GET", "POST"])
def top_margin_degc_view():
    if request.method == 'POST':
        value = request.get_json()['value']
        try:
            thermostat.attributes['top_margin_degc'] = float(value)
        except ValueError:
            return "Invalid value", 400
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

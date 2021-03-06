import os
import random
import string

import netifaces as ni
from datetime import datetime
from flask import Blueprint, request, redirect, url_for, jsonify
from flask.ext.login import login_user, logout_user

from pasteur.extensions import cache, thermostat
from pasteur.forms import LoginForm
from pasteur.models import db, User, Run

main = Blueprint('main', __name__)

api_keys = {}

@main.route('/api/v1')
@cache.cached(timeout=1000)
def home():
    return "Pasteur API root V1."


def _verify_api_key(request):
    try:
        user_id = request.get_json()['user_id']
        api_key = request.get_json()['api_key']
    except KeyError:
        return False
    if user_id in api_keys and api_key in api_keys[user_id]:
        return True
    else:
        return False


@main.route('/api/v1/run', methods=["GET", "POST"])
def run_view():
    if request.method == 'GET':
        return "Not implemented yet", 501
    if request.method == 'POST':
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        try:
            name = request.get_json()['name']
            enabled = request.get_json()['enabled']
        except KeyError:
            return "Bad message", 400
        if enabled:
            log_file_name = '{}_{}'.format(datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), name)
            if 'root' in os.path.expanduser('~'):
                log_file_path = '/var/log/'
            else:
                log_file_path = os.path.expanduser('~/Desktop/')
            run = Run()
            run.name = name
            run.log_file_path = '{}{}'.format(log_file_path, log_file_name)
            db.session.add(run)
            db.session.commit()
            thermostat.attributes['run_name'] = log_file_name
            thermostat.attributes['log_file_path'] = log_file_path
            with open('{}{}.csv'.format(log_file_path, log_file_name), 'w') as f:
                for key in sorted(thermostat.attributes.keys()):
                    f.write('{},'.format(key))
                f.write('\n')
            thermostat.attributes['run_enabled'] = True
            return "Created run {}".format(name)
        else:
            src = '{}{}.csv'.format(thermostat.attributes['log_file_path'], thermostat.attributes['run_name'])
            if 'root' in os.path.expanduser('~'):
                upload_dest = os.path.expanduser('/home/pi/Desktop/run_uploads/{}.csv'.format(thermostat.attributes['run_name']))
            else:
                upload_dest = os.path.expanduser('~/Desktop/run_uploads/{}.csv'.format(thermostat.attributes['run_name']))
            os.rename(src, upload_dest)
            thermostat.attributes['log_file_path'] = '/tmp/'
            thermostat.attributes['run_name'] = 'tmp_no_run'
            thermostat.attributes['run_enabled'] = False
            thermostat.attributes['degc_minutes'] = 0
            return "Cancelled run {}".format(name)


@main.route('/api/v1/sys-info', methods=["GET"])
def sys_info_view():
    ret = {};
    ret['version'] = '0.3.0'
    try:
        ni.ifaddresses('wlan0')
        ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        ret['ipaddr'] = ip
    except ValueError:
        ret['ipaddr'] = 'unknown'
    return jsonify(ret)


@main.route('/api/v1/thermostat-enabled', methods=["GET", "POST"])
def enabled_view():
    if request.method == 'POST':
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
        value = request.get_json()['value']
        thermostat.attributes['thermostat_enabled'] = value
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['enabled']})


@main.route('/api/v1/target-temp-degc', methods=["GET", "POST"])
def target_tempc_view():
    if request.method == 'POST':
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
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
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
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
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
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
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
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
        if not _verify_api_key(request):
            return "Permission to API denied", 403
        if 'value' not in request.get_json(): return "Bad message", 400
        value = request.get_json()['value']
        try:
            thermostat.attributes['top_margin_degc'] = float(value)
        except ValueError:
            return "Invalid value", 400
        print(value)
        return "Ok"
    if request.method == 'GET':
        return jsonify({'value': thermostat.attributes['top_margin_degc']})


@main.route("/get-api-key", methods=["POST"])
def api_key_view():
    if 'username' not in request.get_json(): return "Bad message", 400
    username = request.get_json()['username']
    if 'password' not in request.get_json(): return "Bad message", 400
    password = request.get_json()['password']
    user = User.query.filter_by(username=username).first()
    if not user:
        return "Invalid credentials", 403
    if user.check_password(password):
        key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(24))
        if user.id not in api_keys:
            api_keys[user.id] = [key]
        else:
            api_keys[user.id].append(key)
        return jsonify({'user_id': user.id, 'api_key': key})
    else:
        return "Invalid credentials", 403


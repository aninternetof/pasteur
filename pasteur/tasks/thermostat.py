import random
from flask import json
from datetime import datetime

class Thermostat:

    def __init__(self, socketio):
        self.socketio = socketio
        self.attributes = {
            'tempc_reading': -1,
            'period': 5,
            'target_tempc': -1,
            'target_degc_sec': -1,
            'top_margin_degc': -1,
            'bottom_margin_degc': -1,
            'enabled': False,
            'pump_on': False,
            'timestamp': None,
            'run_name': '',
            'log_file_path': '/tmp/test.log'
        }

    def run_thermostat(self):
        while True:
            print("Taking reading.")
            self.attributes['tempc_reading'] = random.randint(0,100)
            self.attributes['timestamp'] = datetime.now()
            print(json.dumps(self.attributes))
            with open(self.attributes['log_file_path'], 'a') as f:
                f.write(json.dumps(self.attributes)+'\n')
            self.socketio.sleep(self.attributes['period'])

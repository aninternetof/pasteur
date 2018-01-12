import random
from flask import json
from datetime import datetime

class Thermostat:

    def __init__(self, socketio):
        self.socketio = socketio
        self.attributes = {
            'tempf_reading': -1,
            'period': 5,
            'target_tempf': -1,
            'target_degf_sec': -1,
            'enabled': False,
            'pump_on': False,
            'timestamp': None,
        }

    def run_thermostat(self):
        while True:
            print("Taking reading.")
            self.attributes['tempf_reading'] = random.randint(0,100)
            self.attributes['timestamp'] = datetime.now()
            print(json.dumps(self.attributes))
            self.socketio.sleep(self.attributes['period'])

import random
from flask import json
from datetime import datetime

try:
    from gpiozero import LED
except Exception:
    print("Failed to load gpiozero. But not be on Raspberry Pi")



class Thermostat:

    def __init__(self, socketio):
        self.socketio = socketio
        try:
            self.pump = LED(21)
        except NameError:
            pass
        self.attributes = {
            'temp_reading_degc': -1,
            'period': 5,
            'target_temp_degc': 50,
            'target_degc_sec': -1,
            'top_margin_degc': 1,
            'bottom_margin_degc': 1,
            'enabled': True,
            'pump_on': False,
            'timestamp': None,
            'run_name': '',
            'log_file_path': '/tmp/pasteur_no_run.log'
        }

    def run_thermostat(self):
        while True:
            print("Taking reading.")
            self.attributes['tempc_reading'] = random.randint(0,100)
            self.attributes['timestamp'] = datetime.now()
            print(json.dumps(self.attributes))
            if self.attributes['enabled']:
                a = self.attributes
                # TODO: a[temp_reading_degc] =
                if (a['temp_reading_degc'] < (a['target_temp_degc'] - a['bottom_margin_degc'])):
                    try:
                        self.pump.on();
                    except AttributeError:
                        print("Not on Raspberry Pi. Cannot turn pump on.")
                    a['pump_on'] = True
                elif (a['temp_reading_degc'] > (a['target_temp_degc'] + a['bottom_margin_degc'])):
                    try:
                        self.pump.off();
                    except AttributeError:
                        print("Not on Raspberry Pi. Cannot turn pump off.")
                    a['pump_on'] = False
                with open(self.attributes['log_file_path'], 'a') as f:
                    f.write(json.dumps(self.attributes)+'\n')
                self.socketio.emit('log', json.dumps(self.attributes))
            self.socketio.sleep(self.attributes['period'])

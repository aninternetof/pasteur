import random
from flask import json
from datetime import datetime

try:
    from w1thermsensor import W1ThermSensor
except Exception:
    print("Failed to load W1ThermSensor. Apparently we're not on a Raspberry Pi")
try:
    from gpiozero import LED
except Exception:
    print("Failed to load gpiozero. Apparently we're not on a Raspberry Pi")



class Thermostat:

    def __init__(self, socketio):
        self.socketio = socketio
        try:
            self.sensor = W1ThermSensor()
        except NameError:
            pass
        try:
            self.pump = LED(21)
        except NameError:
            pass
        self.attributes = {
            'temp_reading_degc': -1,
            'period_s': 5,
            'target_temp_degc': 100,
            'target_degc_minutes': 3000,
            'degc_minutes': 0,
            'top_margin_degc': 1,
            'bottom_margin_degc': 1,
            'enabled': False,
            'pump_on': False,
            'timestamp': None,
            'run_name': '',
            'log_file_path': '/tmp/pasteur_no_run.log'
        }

    def run_thermostat(self):
        while True:
            print("Taking reading.")
            try:
                self.attributes['temp_reading_degc'] = self.sensor.get_temperature()
            except AttributeError:
                print("Not on Raspberry Pi. Generating random temperature.")
                self.attributes['temp_reading_degc'] = random.randint(0, 200)
            self.attributes['timestamp'] = datetime.now()

            if self.attributes['enabled']:
                if self.attributes['temp_reading_degc'] < \
                        (self.attributes['target_temp_degc'] - self.attributes['bottom_margin_degc']):
                    try:
                        self.pump.on()
                    except AttributeError:
                        print("Not on Raspberry Pi. Cannot turn pump on.")
                    self.attributes['pump_on'] = True
                elif self.attributes['temp_reading_degc'] > \
                        (self.attributes['target_temp_degc'] + self.attributes['top_margin_degc']):
                    try:
                        self.pump.off()
                    except AttributeError:
                        print("Not on Raspberry Pi. Cannot turn pump off.")
                    self.attributes['pump_on'] = False
                self.attributes['degc_minutes'] += self.attributes['temp_reading_degc'] * self.attributes['period_s']/60.0

                if self.attributes['degc_minutes'] >= self.attributes['target_degc_minutes']:
                    try:
                        self.pump.off()
                    except AttributeError:
                        print("Not on Raspberry Pi. Cannot turn pump off.")
                    self.attributes['enabled'] = False
                    self.attributes['degc_minutes'] = 0
                    self.attributes['run_name'] = ''
                    self.attributes['log_file_path'] = '/tmp/pasteur_no_run.log'
                    self.socketio.emit('event', json.dumps({'type': 'done'}))

                with open(self.attributes['log_file_path'], 'a') as f:
                    f.write(json.dumps(self.attributes)+'\n')

            self.socketio.emit('log', json.dumps(self.attributes))
            print(json.dumps(self.attributes))

            self.socketio.sleep(self.attributes['period_s'])

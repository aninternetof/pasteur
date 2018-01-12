class Thermostat:

    def __init__(self, socketio):
        self.socketio = socketio
        self.target_value = 22

    def run_thermostat(self):
        while True:
            print("Hi")
            print(self.target_value)
            self.socketio.sleep(5)

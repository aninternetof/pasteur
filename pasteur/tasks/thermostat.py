from pasteur.extensions import socketio

def run_thermostat():
    while True:
        print("Hi")
        socketio.sleep(1)

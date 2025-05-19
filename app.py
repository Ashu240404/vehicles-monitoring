from flask import Flask, render_template, redirect, url_for
from threading import Thread
from vehicle_monitor import run_vehicle_monitor

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-camera')
def start_camera():
    # Run camera processing in a separate thread to avoid blocking
    thread = Thread(target=run_vehicle_monitor)
    thread.start()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

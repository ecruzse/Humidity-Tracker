from flask import Flask
import json

app = Flask(__name__)

@app.route("/")
def home():
    return 'hi'

@app.route("/metrics")
def metrics():
    return json.dumps({
    "humidity": "",
    "temperature": ""})
    
app.run('0.0.0.0', 5001, True)
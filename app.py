from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    with open('results/summary.json', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/speed_data')
def speed_data():
    with open('results/speed_data.json', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

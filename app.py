from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/employees/', methods=['GET'])
def list_employee():
    return jsonify({'msg': 'hello'}), 200

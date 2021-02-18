from flask import request, jsonify

from src.accountment import app


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        'error': 'Not Found',
        'status': '404',
        'method': request.method,
        'message': error.description,
        'path': request.path,
    }), 404


@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        'error': 'Bad Request',
        'status': '400',
        'method': request.method,
        'messages': error.description,
        'path': request.path,
    }), 400

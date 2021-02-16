from flask import request, jsonify

from src.accounting import app, db
from src.accounting.models import Job, Employee
from src.accounting.schemas import JobSchema, AssignSchema


@app.route('/jobs/<int:pk>/assign_customer', methods=['POST'])
def assign_customer(pk: int):
    job = Job.query.get(pk)
    errors = AssignSchema().validate(request.json)
    if errors:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': errors,
            'path': request.path,
        }), 400

    if not job:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "A job doesn't exist.",
            'path': request.path,
        }), 404

    job.customer_id = request.json['customer_id']
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 201


@app.route('/jobs/<int:pk>/assign_employee', methods=['POST'])
def assign_employee(pk: int):
    job = Job.query.get(pk)
    errors = AssignSchema().validate(request.json)
    if errors:
        return jsonify({
            'error': 'Bad Request',
            'status': '400',
            'method': request.method,
            'messages': errors,
            'path': request.path,
        }), 400

    if not job:
        return jsonify({
            'error': 'Not Found',
            'status': '404',
            'method': request.method,
            'message': "A job doesn't exist.",
            'path': request.path,
        }), 404

    employee = Employee.query.get(request.json['employee_id'])
    job.employees.append(employee)
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 201

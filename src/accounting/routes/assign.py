from typing import Tuple

from flask import request, jsonify, abort, Response

from src.accounting import app, db
from src.accounting.models import Job, Employee
from src.accounting.schemas import JobSchema, AssignSchema


@app.route('/jobs/<int:pk>/assign_customer', methods=['POST'])
def assign_customer(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    if not job:
        abort(404, "A job doesn't exist.")

    errors = AssignSchema().validate(request.json)
    if errors:
        abort(400, errors)

    job.customer_id = request.json['customer_id']
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 201


@app.route('/jobs/<int:pk>/assign_employee', methods=['POST'])
def assign_employee(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    if not job:
        abort(404, "A job doesn't exist.")

    errors = AssignSchema().validate(request.json)
    if errors:
        abort(400, errors)

    employee = Employee.query.get(request.json['employee_id'])
    job.employees.append(employee)
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 201


@app.route('/jobs/<int:pk>/reassign_customer', methods=['PATCH'])
def reassign_customer(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    if not job:
        abort(404, "A job doesn't exist.")

    errors = AssignSchema().validate(request.json)
    if errors:
        abort(400, errors)

    job.customer_id = request.json['customer_id']
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 200


@app.route('/jobs/<int:pk>/unassign_employee', methods=['DELETE'])
def unassign_employee(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    if not job:
        abort(404, "A job doesn't exist.")

    errors = AssignSchema().validate(request.json)
    if errors:
        abort(400, errors)

    employee = Employee.query.get(request.json['employee_id'])
    job.employees.remove(employee)
    db.session.add(job)
    db.session.commit()

    result = JobSchema().dump(job)

    return jsonify(result), 200

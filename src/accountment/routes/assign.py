from typing import Tuple

from flask import request, jsonify, abort, Response

from src.accountment import app, db
from src.accountment.models import Job, Employee
from src.accountment.schemas import JobSchema, AssignSchema


@app.route('/jobs/<int:pk>', methods=['PATCH'])
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

    return jsonify(result), 200


@app.route('/jobs/<int:pk>/assignment', methods=['POST'])
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

    return jsonify(result), 200


@app.route('/jobs/<int:pk>/unassignment', methods=['POST'])
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

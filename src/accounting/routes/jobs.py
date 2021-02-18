from datetime import date, time
from typing import Tuple

from flask import jsonify, request, Response, abort
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Job, Customer
from src.accounting.schemas import JobSchema, AssignSchema
from src.accounting.utils import update_person, update_the_job


@app.route('/jobs', methods=['GET'])
def list_jobs() -> Tuple[Response, int]:
    jobs = Job.query.all()
    jobs_schema = JobSchema(many=True)

    result = jobs_schema.dump(jobs)

    return jsonify(result), 200


@app.route('/jobs/<int:pk>', methods=['GET'])
def retrieve_job(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    job_schema = JobSchema()
    if not job:
        abort(404, "A job doesn't exist.")

    result = job_schema.dump(job)

    return jsonify(result), 200


@app.route('/jobs', methods=['POST'])
def create_job() -> Tuple[Response, int]:
    job_schema = JobSchema()
    errors = job_schema.validate(request.json)
    if errors:
        abort(400, errors)

    date_formatted = date.fromisoformat(request.json['date'])
    start_time_formatted = time.fromisoformat(request.json['start_time'])

    job = Job(
        date=date_formatted,
        start_time=start_time_formatted,
        hours_number=request.json['hours_number'],
    )
    db.session.add(job)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 201


@app.route('/jobs/<int:pk>', methods=['PUT'])
def update_job(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    job_schema = JobSchema()
    if not job:
        abort(404, "A job doesn't exist.")

    errors = job_schema.validate(request.json)
    if errors:
        abort(400, errors)

    update_the_job(job, request.json)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 200


@app.route('/jobs/<int:pk>', methods=['DELETE'])
def destroy_job(pk: int) -> Tuple[Response, int]:
    job = Job.query.get(pk)
    job_schema = JobSchema()
    if not job:
        abort(404, "A job doesn't exist.")

    db.session.delete(job)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 200


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

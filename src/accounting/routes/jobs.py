from datetime import date, time

from flask import jsonify, request
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Job
from src.accounting.schemas import JobSchema
from src.accounting.utils import update_person, update_job


@app.route('/jobs', methods=['GET'])
def list_jobs():
    jobs = Job.query.all()
    jobs_schema = JobSchema(many=True)

    result = jobs_schema.dump(jobs)

    return jsonify(result), 200


@app.route('/jobs/<int:pk>', methods=['GET'])
def retrieve_job(pk):
    job = Job.query.get(pk)
    job_schema = JobSchema()
    if not job:
        return jsonify({'error': {'detail': "A job doesn't exists"}}), 404

    result = job_schema.dump(job)

    return jsonify(result), 200


@app.route('/jobs', methods=['POST'])
def create_job():
    job_schema = JobSchema()
    try:
        job_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    date_formatted = date.fromisoformat(request.json['date'])
    start_time_formatted = time.fromisoformat(request.json['start_time'])

    job = Job(
        customer=request.json['customer'],
        employees=request.json['employees'],
        date=date_formatted,
        start_time=start_time_formatted,
        hours_number=request.json['hours_number'],
    )
    db.session.add(job)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 201


@app.route('/jobs/<int:pk>', methods=['PATCH'])
def partial_update_jobs(pk):
    job = Job.query.get(pk)
    job_schema = JobSchema()
    if not job:
        return jsonify({'error': {'detail': "A job doesn't exists"}}), 404

    try:
        job_schema.load(request.json, partial=True)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    update_job(job, request.json)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 200

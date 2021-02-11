from datetime import date, time

from flask import jsonify, request
from marshmallow import ValidationError

from src.accounting import app, db
from src.accounting.models import Job
from src.accounting.schemas import JobSchema
from src.accounting.utils import update_model


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
        return jsonify({'error': {'detail': "A job doesn't exists"}})

    result = job_schema.dump(job)

    return jsonify(result), 200


@app.route('/jobs', methods=['POST'])
def create_job():
    job_schema = JobSchema()
    try:
        job_schema.load(request.json)

    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    date_formatted = date.fromisoformat(request.json.get('date'))
    start_time_formatted = time.fromisoformat(request.json.get('start_time'))

    job = Job(
        customer=request.json.get('customer'),
        employees=request.json.get('employees'),
        date=date_formatted,
        start_time=start_time_formatted,
        hours_number=request.json.get('hours_number'),
    )
    db.session.add(job)
    db.session.commit()

    result = job_schema.dump(job)

    return jsonify(result), 201

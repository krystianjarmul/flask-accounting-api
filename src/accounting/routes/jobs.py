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


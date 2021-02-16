from datetime import date, time
from typing import List

from . import Employee
from .. import db

assignments = db.Table(
    'assignments',
    db.Column('job_id', db.Integer, db.ForeignKey('job.id')),
    db.Column(
        'employee_id',
        db.Integer,
        db.ForeignKey('employee.id'),
    )
)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    hours_number = db.Column(db.Float)

    employees = db.relationship(
        'Employee',
        secondary='assignments',
        passive_deletes=True
    )

    def __init__(
            self,
            date: date,
            start_time: time,
            hours_number: float
    ):
        self.date = date
        self.start_time = start_time
        self.hours_number = hours_number

    def __repr__(self) -> str:
        return f'Job id: {self.id}'

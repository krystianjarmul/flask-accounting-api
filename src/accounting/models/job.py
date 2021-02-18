from datetime import date, time, datetime, timedelta
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
        self.end_time = self._get_end_time()

    def _get_end_time(self):
        dt = datetime.combine(self.date, self.start_time) + timedelta(
            hours=int(self.hours_number),
            minutes=int((self.hours_number % 1) * 60)
        )
        return dt.time()

    def __repr__(self) -> str:
        return f'Job id: {self.id}'

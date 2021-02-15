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
    employee_ids = db.Column(db.String)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    hours_number = db.Column(db.Float)

    customer = db.relationship('Customer', backref='jobs', cascade='all')
    employees = db.relationship(
        'Employee',
        secondary='assignments',
        backref=db.backref('jobs', lazy='dynamic'),
        cascade='all'
    )

    def __init__(
            self,
            customer_id: int,
            employee_ids: List[int],
            date: date,
            start_time: time,
            hours_number: float
    ):
        self.customer_id = customer_id
        self._employee_ids = employee_ids
        self.date = date
        self.start_time = start_time
        self.hours_number = hours_number
        self.employee_ids = self._employee_ids_to_string()

        self._assign_employees()

    def _employee_ids_to_string(self):
        if isinstance(self._employee_ids, str):
            self._employee_ids = self._employee_ids.split(',')
        return ','.join([str(e) for e in self._employee_ids])

    def _assign_employees(self):
        for employee_id in self._employee_ids:
            employee = Employee.query.get(employee_id)
            if employee:
                self.employees.append(employee)
        db.session.commit()

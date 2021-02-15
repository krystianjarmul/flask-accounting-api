from datetime import date, time
from typing import List

from .. import db


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    employees = db.Column(db.String)
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    hours_number = db.Column(db.Float)

    def __init__(
            self,
            customer_id: int,
            employees: List[int],
            date: date,
            start_time: time,
            hours_number: float
    ):
        self.customer_id = customer_id
        self._employees = employees
        self.date = date
        self.start_time = start_time
        self.hours_number = hours_number
        self.employees = self._employees_to_string()

    def _employees_to_string(self):
        if isinstance(self._employees, str):
            self._employees = self._employees.split(',')
        return ','.join([str(e) for e in self._employees])

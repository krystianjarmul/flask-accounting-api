from .. import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    jobs = db.relationship(
        'Job',
        secondary='assignments',
        passive_deletes=True,
        lazy='subquery'
    )

    def __init__(self, name: str):
        self.name = name

    @property
    def hours_number(self) -> float:
        if not self.jobs:
            return 0
        return sum(j.hours_per_employee for j in self.jobs)

    def __repr__(self) -> str:
        return f'Employee id: {self.id} name: {self.name}'

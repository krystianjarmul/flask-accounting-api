from .. import db


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    jobs = db.relationship(
        'Job',
        secondary='assignments',
        passive_deletes=True
    )

    def __init__(self, name: str):
        self.name = name

    def __repr__(self) -> str:
        return f'Employee id: {self.id} name: {self.name}'

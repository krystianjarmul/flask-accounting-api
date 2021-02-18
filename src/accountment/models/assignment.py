from src.accountment import db


class Assignment(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    job_id = db.Column('job_id', db.Integer, db.ForeignKey('job.id'))
    employee_id = db.Column(
        'employee_id',
        db.Integer,
        db.ForeignKey('employee.id')
    )

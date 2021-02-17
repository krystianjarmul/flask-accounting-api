import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from src.accounting import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def test():
    flask_env = os.environ.get('FLASK_ENV')
    os.environ['FLASK_ENV'] = 'testing'
    os.system('pytest')
    os.environ['FLASK_ENV'] = flask_env


if __name__ == '__main__':
    manager.run()

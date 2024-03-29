import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

# SQL Alchemy connects to the Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

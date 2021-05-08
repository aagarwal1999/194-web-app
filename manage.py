from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import load_config, get_log_folder, get_mysql_config
from pbu import Logger
from storage.shared import db
from storage.models.dataset import Dataset


# load config from .env file
config = load_config()

# ---- database and stores ----

host, db_name, username, password = get_mysql_config()
uri = 'mysql://{0}:{1}@{2}/{3}'.format(username, password, host, db_name)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
db.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':

    logger = Logger("DB", log_folder=get_log_folder())
    manager.run()
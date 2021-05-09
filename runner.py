from flask import Flask
# TODO: clean up unused imports
from pbu import Logger
from storage.shared import db
from config import load_config, get_log_folder, get_mysql_config
from flask_migrate import Migrate
import api.static_api as static_api
import api.model_api as model_api

if __name__ == "__main__":
    logger = Logger("MAIN", log_folder=get_log_folder())
    logger.info("==========================================")
    logger.info("           Starting application")
    logger.info("==========================================")

    # load config from .env file
    config = load_config()

    # ---- database and stores ----

    # create mysql connection (TODO: remove this block or uncomment)
    host, db_name, username, password = get_mysql_config()
    uri = 'mysql://{0}:{1}@{2}/{3}'.format(username, password, host, db_name)

    # create flask app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    db.init_app(app)

    # register endpoints
    static_api.register_endpoints(app)
    # TODO: replace this with your (multiple) API registrations
    model_api.register_endpoints(app, db.session)

    # start flask app
    app.run(host='0.0.0.0', port=5555, debug=config["IS_DEBUG"])

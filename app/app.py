import logging
import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from textwrap import wrap

from .database import db
from .config import Config

app = Flask('app')


class MaxLengthFormatter(logging.Formatter):
    def __init__(self, max_length=120, *args):
        super().__init__(*args)
        self.max_length = max_length

    def format(self, record):
        msg = "\n".join(wrap(super().format(record), self.max_length))
        return msg


new_handler = logging.FileHandler(
    filename=os.getcwd() + '/app.log')
new_handler.setLevel(logging.INFO)
new_handler_formatter = MaxLengthFormatter(
    80,
    '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
new_handler.setFormatter(new_handler_formatter)
app_handler = new_handler

app.logger = logging.Logger('app')
app.logger.handlers.clear()
app.logger.addHandler(app_handler)

app.logger.info(f'new app {app} successfully initialized')

app.config.from_object(Config)
app.logger.info(f'new config {app.config} successfully adopted')

migrate = Migrate(app, db.db)
db.db.init_app(app)
app.logger.info(f'new db {db.db} successfully created within {app} context')

with app.app_context():
    db.db.create_all()
    app.logger.info('tables inside db created')

csrf = CSRFProtect(app)
app.logger.info(f'CSRF protection working')

app.logger.info(f'current path is {str(app.instance_path)}')

with app.app_context():
    from .admin import *
    app.logger.info(f'current admin is {admin}')

from .routes import *

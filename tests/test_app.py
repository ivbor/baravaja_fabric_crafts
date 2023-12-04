import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def test_can_import_app():

    import app

    assert hasattr(app, 'app'), \
        'file app.py inside module app has not been created'


def test_app_created():

    from app import app

    assert isinstance(app.app, Flask)
    assert app.app.import_name == 'app', \
        'app does not have the name app'


def test_logger_configured():

    from app.app import app_handler

    existing_handler = app_handler
    test_logger = logging.Logger('test_logger')
    test_logger.addHandler(existing_handler)
    open('app.log', 'w').close()
    test_logger.info('this is first log')
    test_logger.handlers.clear()
    with open('app.log', 'r') as file:
        assert 'this is first log' in file.readline()


def test_config_from_object():

    from app.app import app
    from app.config import Config

    for attr in dir(Config):
        if '__' not in attr and attr != 'mro':
            assert getattr(Config, attr) == app.config[attr]


def test_db_exists():

    from app.database import db, Database

    assert isinstance(db, Database)
    assert isinstance(db.db, SQLAlchemy)


def test_db_works():

    from app.app import app

    with app.app_context():

        from app.database import db
        from app.models import Good, Order, User

        db.db.init_app(app)
        db.db.create_all()
        models = db.db.Model.__subclasses__()
        assert Good in models
        assert Order in models
        assert User in models

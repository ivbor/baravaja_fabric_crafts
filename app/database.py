"""
Database interface initialization
"""
from flask_sqlalchemy import SQLAlchemy

from .models import db


class Database():

    def __init__(self, db: SQLAlchemy):
        self.db = db

    def delete_all_tables(self):
        self.db.drop_all()

    def table_is_model(self, table_name):
        if not issubclass(table_name, SQLAlchemy.Model):
            raise TypeError(
                f'class {table_name} has to be ' +
                'the subclass of SQLAlchemy.Model')
        else:
            return True

    def db_connected_to_app(self):
        exc_msg = \
            'db.session does not have a connection to any database' +\
            ', try using db.init_app() before using database'
        try:
            if db.db.session.bind is None:
                raise Exception(exc_msg)
        except RuntimeError:
            raise AttributeError(exc_msg)

    def delete_table(self, table_name):
        if self.table_is_model(table_name) and self.db_connected_to_app():
            table_name.__table__.drop(self.db.session.bind)

    def add_table(self, table_name):
        if self.table_is_model(table_name) and self.db_connected_to_app():
            table_name.__table__.create(self.db.session.bind)


db = Database(db)

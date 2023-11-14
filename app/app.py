import logging

from flask_login import LoginManager, login_required, login_user, logout_user
from flask_session import Session

from .config import Config
from .routes import app
from .models import db, User

# Logging Basic Config
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize Flask app
logging.info(f'new app {app} successfully initialized')

# Change this to a strong, random key
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
app.logger.info(f'new login {login_manager} successfully created')

# Use app context
db.init_app(app)
app.logger.info(f'new db {db} successfully created within {app} context')
app.logger.info(str(app.instance_path))

with app.app_context():
    db.create_all()
    app.logger.info('tables inside db created')

# Initialize session
Session(app)

# functions making interface with database


def drop_tables():
    db.drop_all()


def get_all(table_name):
    return [entry for entry in table_name.Query.all()]


def add(table_name, db, **kwargs):
    new_entry = table_name()
    for item in kwargs.items():
        new_entry.__setattr__(item[0], item[1])
        if new_entry:
            logging.info(f'new entry {new_entry} for the table' +
                         f'{table_name} created')
    db.session.add(new_entry)
    logging.info(f'new entry {new_entry} added to the table {table_name}')
    db.session.commit()


def update(table_name, by, db, **kwargs):
    for item in kwargs.items():
        if by == item[0]:
            entries_to_change = \
                table_name.Query.filter_by(item[0] == item[1]).all()
        break
    for entry in entries_to_change:
        for item in kwargs.items():
            if entry.__getattr__(item[0]) != item[1]:
                entry.__setattr__(item[0], item[1])
    db.session.commit()


def delete(table_name, condition, db):
    entries_to_delete = table_name.Query.filter_by(condition).all()
    for entry in entries_to_delete:
        db.session.delete(entry)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

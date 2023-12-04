from werkzeug.security import generate_password_hash

from .app import db
from .models import User

admin = User.query.filter_by(email='admin').first()

if admin is not None:
    admin.is_admin = True
else:
    admin = User(email='admin',
                 hashed_password=generate_password_hash('password'),
                 is_admin=True)
    db.db.session.add(admin)
db.db.session.commit()

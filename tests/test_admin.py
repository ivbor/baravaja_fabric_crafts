from app.app import app


def test_admin_exists():

    with app.app_context():

        from app.models import User

        user = User.query.filter_by(email='admin').first()
        assert user is not None
        assert user.email == 'admin'
        assert user.is_admin is True

import pytest

from flask.testing import FlaskClient

from app.routes import app


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    return app.test_client()


def test_empty_route(client):
    response = client.get('/')
    assert response.status_code == 302
    assert '/home' in str(response.data)


def test_index_route(client):
    response = client.get('/index')
    assert response.status_code == 302
    assert '/home' in str(response.data)


def test_home_route(client):
    with app.test_request_context():
        response = client.get('/home')
        assert response.status_code == 200
        data = str(response.data)
        # check if styles loaded
        assert 'styles.css' in data
        # check if index.html loaded
        assert 'index.js' in data
        # check if header.html loaded
        assert 'header.js' in data
        # check if footer.html loaded
        assert 'copyright' in data

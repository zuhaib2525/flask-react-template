import pytest
import sys
import os

# Add 'backend' folder to sys.path for imports in tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app import app as flask_app, db
from models import Task

@pytest.fixture(scope='session')
def app():
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    with flask_app.app_context():
        db.create_all()
        # Create sample data once per test session
        task = Task(title='Test Task')
        db.session.add(task)
        db.session.commit()
    yield flask_app
    with flask_app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

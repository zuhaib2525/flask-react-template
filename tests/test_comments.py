import pytest
from app import app, db
from models import Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Insert a sample task for comment tests
            task = Task(title='Test Task')
            db.session.add(task)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()


def test_create_comment(client):
    rv = client.post('/tasks/1/comments', json={'content': 'Hello'})
    assert rv.status_code == 201
    data = rv.get_json()
    assert data['content'] == 'Hello'
    assert data['task_id'] == 1


def test_get_comments(client):
    client.post('/tasks/1/comments', json={'content': 'Comment 1'})
    client.post('/tasks/1/comments', json={'content': 'Comment 2'})
    rv = client.get('/tasks/1/comments')
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data) == 2


def test_update_comment(client):
    client.post('/tasks/1/comments', json={'content': 'Old'})
    rv = client.put('/tasks/1/comments/1', json={'content': 'New'})
    assert rv.status_code == 200
    data = rv.get_json()
    assert data['content'] == 'New'


def test_delete_comment(client):
    client.post('/tasks/1/comments', json={'content': 'Delete me'})
    rv = client.delete('/tasks/1/comments/1')
    assert rv.status_code == 200
    assert 'deleted' in rv.get_json()['message'].lower()


def test_create_comment_empty_content(client):
    rv = client.post('/tasks/1/comments', json={'content': ''})
    assert rv.status_code in (400, 422)  # Adjust status code if your app differs


def test_create_comment_missing_content(client):
    rv = client.post('/tasks/1/comments', json={})
    assert rv.status_code == 400  # This code assumes your API returns 400


def test_update_nonexistent_comment(client):
    rv = client.put('/tasks/1/comments/9999', json={'content': 'Update'})
    assert rv.status_code == 404


def test_delete_nonexistent_comment(client):
    rv = client.delete('/tasks/1/comments/9999')
    assert rv.status_code == 404


def test_create_comment_long_content(client):
    long_text = 'a' * 10000
    rv = client.post('/tasks/1/comments', json={'content': long_text})
    assert rv.status_code == 201
    assert rv.get_json()['content'] == long_text

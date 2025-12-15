import pytest 
from app import app, db, Todo

@pytest.fixture
def test_app():
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_add_todo(client):
    # ACTION: SEND POST REQUEST TO /add
    response = client.post(
        "/add",
        data={
            "title": "Test Task",
            "priority": "High"
        },
        follow_redirects=True
    )

    # ASSERT: check database state
    #todo = Todo.query.first()

    todo = Todo.query.filter_by(title="Test Task").one()
    assert todo.priority_level == 3

    assert todo is not None
    assert todo.title == "Test Task"
    assert todo.priority == "High"
    assert todo.priority_level == 3
    assert todo.complete is False
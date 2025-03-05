import pytest
from app import create_app, db
from app.models.user import User


@pytest.fixture
def client():
    app = create_app()

    # Use an in-memory database for testing
    app.config['DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test_jwt_secret_key'

    with app.test_client() as client:
        with app.app_context():
            # Create tables for testing
            db.create_all()  
        yield client
        with app.app_context():
            # Clean up after the test
            db.drop_all() 


# Test user  successful registration
def test_register(client):
    # Test that a new user can register
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['msg'] == 'User created successfully'

    # Test that a duplicate user can't be created
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'anotherpassword'
    })
    data = response.get_json()
    assert response.status_code == 422
    assert 'already exists' in data['msg']


# Test user successful login 
def test_login(client):
    # Register a user first
    client.post('/register', json={
        'username': 'testuser',
        'password': 'testpassword'
    })

    # Test login with correct credentials
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert 'access_token' in data

    # Test login with incorrect credentials
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['msg'] == 'Invalid credentials'

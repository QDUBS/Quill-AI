import pytest
import openai
from app import db
from unittest.mock import patch
from app.models.generated_text import GeneratedText


@pytest.fixture
def mock_openai_response():
    with patch.object(openai.Completion, 'create', return_value={
        'choices': [{'text': 'This is a generated response'}]
    }) as mock:
        yield mock


def test_generate_text(client, mock_openai_response):
    # Assume the user is logged in and has a valid JWT token
    response = client.post('/generate-text', json={
        'prompt': 'What is AI?',
        'user_id': 1
    }, headers={
        'Authorization': 'Bearer test_valid_jwt_token'  # Use a mock token
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Text generated and saved'
    assert data['response'] == 'This is a generated response'


def test_get_generated_text(client):
    # Assume the user has generated text in the system
    generated_text = GeneratedText(
        user_id=1, prompt="What is AI?", response="AI means artificial intelligence.")
    db.session.add(generated_text)
    db.session.commit()

    # Simulate authorized access (correct JWT token)
    response = client.get(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer test_valid_jwt_token'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['prompt'] == "What is AI?"
    assert data['response'] == "AI is artificial intelligence."

    # Simulate unauthorized access (incorrect JWT token)
    response = client.get(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer invalid_jwt_token'
    })
    assert response.status_code == 403
    assert 'Permission denied' in response.get_json()['message']


def test_get_generated_text(client):
    # Assume the user has generated text in the system
    generated_text = GeneratedText(
        user_id=1, prompt="What is AI?", response="AI is artificial intelligence.")
    db.session.add(generated_text)
    db.session.commit()

    # Simulate authorized access (correct JWT token)
    response = client.get(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer test_valid_jwt_token'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['prompt'] == "What is AI?"
    assert data['response'] == "AI is artificial intelligence."

    # Simulate unauthorized access (i.e incorrect JWT token)
    response = client.get(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer invalid_jwt_token'
    })
    assert response.status_code == 403
    assert 'Permission denied' in response.get_json()['message']


def test_update_generated_text(client):
    # Assume user has generated text
    generated_text = GeneratedText(
        user_id=1, prompt="What is AI?", response="Old response")
    db.session.add(generated_text)
    db.session.commit()

    # Simulate updating text with correct permissions
    response = client.put(f'/generated-text/{generated_text.id}', json={
        'prompt': 'What is AI, really?',
        'response': 'Updated response'
    }, headers={'Authorization': 'Bearer test_valid_jwt_token'})
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Text updated successfully'

    # Simulate attempting to update text owned by another user
    response = client.put(f'/generated-text/{generated_text.id}', json={
        'prompt': 'What is AI, really?',
        'response': 'Updated response'
    }, headers={'Authorization': 'Bearer invalid_jwt_token'})
    data = response.get_json()
    assert response.status_code == 403
    assert data['message'] == 'Permission denied'


def test_delete_generated_text(client):
    # Assume user has generated text
    generated_text = GeneratedText(
        user_id=1, prompt="What is AI?", response="Text to be deleted")
    db.session.add(generated_text)
    db.session.commit()

    # Simulate authorized deletion
    response = client.delete(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer test_valid_jwt_token'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Text deleted successfully'

    # Simulate unauthorized deletion (wrong user)
    response = client.delete(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer invalid_jwt_token'
    })
    assert response.status_code == 403
    assert 'Permission denied' in response.get_json()['message']


def test_delete_generated_text(client):
    # Assume user has generated text
    generated_text = GeneratedText(
        user_id=1, prompt="What is AI?", response="Text to be deleted")
    db.session.add(generated_text)
    db.session.commit()

    # Simulate authorized deletion
    response = client.delete(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer test_valid_jwt_token'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Text deleted successfully'

    # Simulate unauthorized deletion (wrong user)
    response = client.delete(f'/generated-text/{generated_text.id}', headers={
        'Authorization': 'Bearer invalid_jwt_token'
    })
    assert response.status_code == 403
    assert 'Permission denied' in response.get_json()['message']

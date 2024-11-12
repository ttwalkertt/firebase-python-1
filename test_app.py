import pytest
from app import app
from datetime import datetime, timezone
import uuid

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upsert_document(client):
    # Generate a UUID for the test
    test_uuid = str(uuid.uuid4())

    # Test creating a new document
    response = client.put('/upsert', json={
        'uuid': test_uuid,  # Use the generated UUID
        'name': 'John Doe',
        'age': 30,
        'creation_timestamp': datetime.now(timezone.utc).isoformat(),
        'user_id': 'user123'
    })
    assert response.status_code == 201
    assert response.json['success'] == True
    assert response.json['message'] == 'Document created'

    # Test updating the existing document
    response = client.put('/upsert', json={
        'uuid': test_uuid,  # Use the same UUID
        'name': 'John Doe',
        'age': 31,
        'creation_timestamp': datetime.now(timezone.utc).isoformat(),
        'user_id': 'user123'
    })
    assert response.status_code == 200
    assert response.json['success'] == True
    assert response.json['message'] == 'Document updated'

def test_get_document(client):
    # Test getting the document
    response = client.get('/get/John Doe')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]['name'] == 'John Doe'

def test_delete_document(client):
    # Test deleting the document
    response = client.delete('/delete/John Doe')
    assert response.status_code == 200
    assert response.json['success'] == True

    # Test deleting a non-existent document
    response = client.delete('/delete/NonExistent')
    assert response.status_code == 404
    assert response.json['error'] == 'Document not found'

def test_list_documents(client):
    # Test listing documents
    response = client.get('/list')
    assert response.status_code == 200
    assert isinstance(response.json, list)
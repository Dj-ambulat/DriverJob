import pytest
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 200
    assert b'Road Fighters' in resp.data

def test_login_page(client):
    resp = client.get('/auth/login')
    assert resp.status_code == 200

def test_register_page(client):
    resp = client.get('/auth/register')
    assert resp.status_code == 200

def test_vacancies_page(client):
    resp = client.get('/vacancies')
    assert resp.status_code == 200

def test_resumes_page(client):
    resp = client.get('/resumes', follow_redirects=True)
    # Для неавторизованных — редирект на логин или 200 с текстом
    assert resp.status_code in (200, 302) 
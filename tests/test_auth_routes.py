from werkzeug.security import generate_password_hash
from app.models import User, db

def test_login_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_register_user(client, app):
    response = client.post("/register", data={
        "username": "new",
        "password": "123"
    })
    assert response.status_code == 302

def test_login_success(client, app):
    user = User(
        username="test",
        password_hash=generate_password_hash("123")
    )
    db.session.add(user)
    db.session.commit()

    response = client.post("/", data={
        "username": "test",
        "password": "123"
    })
    assert response.status_code == 302

def test_login_fail(client):
    response = client.post("/", data={
        "username": "bad",
        "password": "bad"
    })
    assert response.status_code == 200

def test_logout_requires_login(client):
    response = client.get("/logout")
    assert response.status_code == 302

def test_logout(client, admin_user):
    client.post("/", data={"username": "admin", "password": "admin123"})
    response = client.get("/logout")
    assert response.status_code == 302

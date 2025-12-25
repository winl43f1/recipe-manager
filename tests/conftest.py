import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import create_app
from app.models import db, User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
        "SECRET_KEY": "test"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def admin_user(app):
    user = User(
        username="admin",
        password_hash=generate_password_hash("admin123"),
        role="admin"
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def normal_user(app):
    user = User(
        username="user",
        password_hash=generate_password_hash("user123"),
        role="user"
    )
    db.session.add(user)
    db.session.commit()
    return user

from app.models import User, Recipe

def test_user_creation(app):
    user = User(username="test", password_hash="hash", role="user")
    assert user.username == "test"

from app.models import db, User

def test_user_default_role(app):
    user = User(username="test", password_hash="hash")
    db.session.add(user)
    db.session.commit()
    assert user.role == "user"


def test_recipe_creation(app):
    recipe = Recipe(title="Soup", category="Food")
    assert recipe.title == "Soup"

def test_recipe_has_category(app):
    recipe = Recipe(category="Dinner")
    assert recipe.category == "Dinner"

def test_recipe_has_ingredients(app):
    recipe = Recipe(ingredients="Water")
    assert recipe.ingredients == "Water"

def test_recipe_user_id(app):
    recipe = Recipe(user_id=1)
    assert recipe.user_id == 1

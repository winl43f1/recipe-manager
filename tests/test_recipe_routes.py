from app.models import Recipe, db

def login(client, username, password):
    return client.post("/", data={
        "username": username,
        "password": password
    })

def test_recipes_requires_login(client):
    response = client.get("/recipes")
    assert response.status_code == 302

def test_recipes_page(client, admin_user):
    login(client, "admin", "admin123")
    response = client.get("/recipes")
    assert response.status_code == 200

def test_add_recipe_admin_only(client, normal_user):
    login(client, "user", "user123")
    response = client.get("/recipes/add")
    assert response.status_code == 302

def test_add_recipe_admin(client, admin_user):
    login(client, "admin", "admin123")
    response = client.post("/recipes/add", data={
        "title": "Soup",
        "category": "Food",
        "ingredients": "Water",
        "description": "Hot"
    })
    assert response.status_code == 302

def test_delete_recipe(client, admin_user, app):
    login(client, "admin", "admin123")
    recipe = Recipe(title="Test")
    db.session.add(recipe)
    db.session.commit()

    response = client.get(f"/recipes/delete/{recipe.id}")
    assert response.status_code == 302

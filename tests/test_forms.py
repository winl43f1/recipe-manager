from app.forms import LoginForm, RecipeForm

def test_login_form_valid(app):
    form = LoginForm(data={"username": "a", "password": "b"})
    assert form.validate()

def test_login_form_invalid(app):
    form = LoginForm(data={"username": ""})
    assert not form.validate()

def test_recipe_form_valid(app):
    form = RecipeForm(data={
        "title": "Cake",
        "category": "Dessert",
        "ingredients": "Sugar",
        "description": "Sweet"
    })
    assert form.validate()

def test_recipe_form_invalid(app):
    form = RecipeForm(data={"title": ""})
    assert not form.validate()

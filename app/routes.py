from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Recipe
from .forms import LoginForm, RecipeForm

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for("main.recipes"))
    return render_template("login.html", form=form)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password_hash=generate_password_hash(request.form["password"]),
            role="user"
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("register.html")

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/recipes")
@login_required
def recipes():
    category = request.args.get("category", "")
    title = request.args.get("title", "")

    query = Recipe.query

    if category:
        query = query.filter(Recipe.category.ilike(f"%{category}%"))

    if title:
        query = query.filter(Recipe.title.ilike(f"%{title}%"))

    recipes = query.all()
    recipes_count = len(recipes)

    return render_template(
        "recipes.html",
        recipes=recipes,
        recipes_count=recipes_count
    )



@main.route("/recipes/add", methods=["GET", "POST"])
@login_required
def add_recipe():
    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))

    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            category=form.category.data,
            ingredients=form.ingredients.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for("main.recipes"))

    return render_template("recipe_form.html", form=form)


@main.route("/recipes/delete/<int:id>")
@login_required
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))

    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for("main.recipes"))



@main.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))
    return render_template("admin.html", users=User.query.all())
@main.route("/recipes/<int:recipe_id>")
@login_required
def recipe_detail(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template("recipe_detail.html", recipe=recipe)
@main.route("/admin/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))

    user = User.query.get_or_404(user_id)

    # защита от удаления самого себя
    if user.id == current_user.id:
        return redirect(url_for("main.admin"))

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("main.admin"))
@main.route("/admin/change_role/<int:user_id>")
@login_required
def change_role(user_id):
    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))

    user = User.query.get_or_404(user_id)

    if user.role == "user":
        user.role = "admin"
    else:
        user.role = "user"

    db.session.commit()
    return redirect(url_for("main.admin"))
@main.route("/recipes/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_recipe(id):
    recipe = Recipe.query.get_or_404(id)

    if current_user.role != "admin":
        return redirect(url_for("main.recipes"))

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.category = form.category.data
        recipe.ingredients = form.ingredients.data
        recipe.description = form.description.data

        db.session.commit()
        return redirect(url_for("main.recipes"))

    return render_template(
        "recipe_form.html",
        form=form,
        edit=True
    )

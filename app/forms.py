from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")

class RecipeForm(FlaskForm):
    title = StringField("Название", validators=[DataRequired()])
    category = StringField("Категория", validators=[DataRequired()])
    ingredients = TextAreaField("Ингредиенты", validators=[DataRequired()])
    description = TextAreaField("Описание", validators=[DataRequired()])
    submit = SubmitField("Сохранить")

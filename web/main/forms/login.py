from flask_wtf import FlaskForm
from wtforms import validators, PasswordField, SubmitField
from wtforms.fields.html5 import EmailField

class Login(FlaskForm):

    email = EmailField(
        label="E-Mail",
        validators=[
            validators.DataRequired(message="Este campo es requerido"),
            validators.Email(message="Formato incorrecto")])
    password = PasswordField(
        label="Contraseña",
        validators=[
            validators.DataRequired(message="Este campo es requerido")])
    submit_button = SubmitField(label="Ingresar")

from flask_wtf import FlaskForm
from wtforms import validators, PasswordField, SubmitField, RadioField
from wtforms.fields.html5 import EmailField

class Login(FlaskForm):

    email = EmailField(
        label="E-Mail",
        validators=[validators.DataRequired(message="Este campo es requerido"),
            validators.Email(message="Formato incorrecto")],
        render_kw={"placeholder": "Username"})
    password = PasswordField(
        label="Contraseña",
        validators=[
            validators.DataRequired(message="Este campo es requerido")],
        render_kw={"placeholder": "Password"})
    submit_button = SubmitField(label="Ingresar")

class Register(FlaskForm):

    email = EmailField(
        label="",
        validators=[
            validators.DataRequired(message="Este campo es obligatorio"),
            validators.EqualTo("re_email", message="Los email deben ser iguales"),
            validators.Email(message="Formato incorrecto")],
        render_kw={"placeholder": "Email"})
    re_email = EmailField(
        label="",
        validators=[
            validators.DataRequired(message="Este campo es obligatorio"),
            validators.Email(message="Formato incorrecto")],
        render_kw={"placeholder": "Repetir Email"})
    password = PasswordField(
        label="",
        validators=[
            validators.DataRequired(message="Este campo es obligatorio"),
            validators.EqualTo("re_password", message="Las contraseñas deben ser iguales")],
        render_kw={"placeholder": "Contraseña"})
    re_password = PasswordField(
        label="",
        validators=[
            validators.DataRequired(message="Este campo es obligatorio")
        ],
        render_kw={"placeholder": "Repetir contraseña"})
    admin_choices = [(1, 'Si'), (0, 'No')]
    admin = RadioField(
        label="",
        validators=[validators.InputRequired(message="Este campo es obligatorio")],
        choices=admin_choices,
        coerce=int)
    submit_button = SubmitField(label="Registrarse")

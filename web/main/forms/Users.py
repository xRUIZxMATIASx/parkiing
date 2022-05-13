from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.fields.html5 import EmailField

class CreateUser(FlaskForm):

    email = EmailField(
        label="",
        validators=[
            wtf.validators.DataRequired(message="Este campo es obligatorio"),
            wtf.validators.Email(message="Formato incorrecto")])
    password = wtf.PasswordField(
        label="",
        validators=[
            wtf.validators.DataRequired(message="Este campo es obligatorio"),
            wtf.validators.EqualTo("re_password", message="Las contraseñas deben ser iguales")])
    re_password = wtf.PasswordField(
        label="",
        validators=[
            wtf.validators.DataRequired(message="Este campo es obligatorio")
        ])
    admin_choices = [(1, 'Si'), (0, 'No')]
    admin = wtf.RadioField(
        label="",
        validators=[wtf.validators.InputRequired(message="Este campo es obligatorio")],
        choices=admin_choices,
        coerce=int)
    submit_button = wtf.SubmitField(label="Agregar Usuario")


class EditUser(FlaskForm):
    email = EmailField(
        label="",
        validators=[
            wtf.validators.DataRequired(message="Este campo es obligatorio"),
            wtf.validators.Email(message="Formato incorrecto")])
    admin_choices = [(1, 'Si'), (0, 'No')]
    admin = wtf.RadioField(
        label="",
        validators=[wtf.validators.InputRequired(message="Este campo es obligatorio")],
        choices=admin_choices,
        coerce=int)
    submit_button = wtf.SubmitField(label="Guardar")

from flask_wtf import FlaskForm
import wtforms as wtf


class CreateParking(FlaskForm):

    name = wtf.StringField(
        label="name",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")],
        render_kw={"placeholder": "Nombre de la playa de estacionamiento"}
    )
    location = wtf.StringField(
        label="location",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")],
        render_kw={"placeholder": "Coordenadas geográficas"}
    )
    space = wtf.IntegerField(
        label="space",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")],
        render_kw={"placeholder": "Ingrese numeros enteros"}
    )
    price = wtf.IntegerField(
        label="price",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")],
        render_kw={"placeholder": "Ej. 119.99"}
    )

    submit_button = wtf.SubmitField(label="Guardar")


from flask_wtf import FlaskForm
import wtforms as wtf
from wtforms.fields.html5 import DateTimeLocalField


class Seism(FlaskForm):
    depth = wtf.IntegerField(
        label="",
        validators=[wtf.validators.DataRequired(message="Debe ser un entero")]
    )
    magnitude = wtf.FloatField(
        label="",
        validators=[wtf.validators.DataRequired(message="Debe ser un entero")]
    )
    status_choices = [(1, 'Si'), (0, 'No')]
    verified = wtf.RadioField(
        label="",
        choices=status_choices,
        validators=[wtf.validators.InputRequired(message="Este campo es obligatorio")],
        coerce=int
    )
    submit_button = wtf.SubmitField(label="Guardar")


class UnverifiedSeismsSearch(FlaskForm):
    seismId = wtf.SelectField(
        label="Nombre Sensor",
        validators=[wtf.validators.optional()],
        coerce=int)
    from_date = DateTimeLocalField(
        label="De",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
    )
    to_date = DateTimeLocalField(
        label="Hasta",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
    )

    order_by = wtf.HiddenField()
    submit_button = wtf.SubmitField(label="Aplicar")


class VerifiedSeismsSearch(FlaskForm):
    from_date = DateTimeLocalField(
        label="De",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
    )
    to_date = DateTimeLocalField(
        label="Hasta",
        validators=[wtf.validators.optional()],
        format='%Y-%m-%d %H:%M:%S'
    )
    depth_min = wtf.IntegerField(
        label="Profundidad minima",
        validators=[wtf.validators.optional()]
    )
    depth_max = wtf.IntegerField(
        label="Profundidad maxima",
        validators=[wtf.validators.optional()]
    )
    magnitude_min = wtf.FloatField(
        label="Magnitud minima",
        validators=[wtf.validators.optional()]
    )
    magnitude_max = wtf.FloatField(
        label="Magnitud maxima",
        validators=[wtf.validators.optional()]
    )
    sensor_name = wtf.SelectField(
        label="Nombre Sensor",
        validators=[wtf.validators.optional()],
        coerce=int)
    order_by = wtf.HiddenField()
    submit_button = wtf.SubmitField(label="Aplicar")
    download = wtf.SubmitField(label="Descargar en CSV")


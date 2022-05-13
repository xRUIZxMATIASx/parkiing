from flask_wtf import FlaskForm
import wtforms as wtf


class CreateSensor(FlaskForm):

    name = wtf.StringField(
        label="",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")]
    )
    ip = wtf.StringField(
        label="",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")]
    )
    port = wtf.IntegerField(
        label="",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")]
    )
    status_choices = [(1, 'Activo'), (0, 'No Activo')]
    status = wtf.RadioField(
        label="",
        choices=status_choices,
        validators=[wtf.validators.InputRequired(message="Este campo es obligatorio")],
        coerce=int
    )
    active_choices = [(1, 'Si'), (0, 'No')]
    active = wtf.RadioField(
        label="",
        choices=active_choices,
        validators=[wtf.validators.InputRequired(message="Este campo es obligatorio")],
        coerce=int
    )
    user_id = wtf.IntegerField(
        label="",
        validators=[wtf.validators.DataRequired(message="Este campo es obligatorio")])
    submit_button = wtf.SubmitField(label="Guardar")


class SensorFilter(FlaskForm):
    name = wtf.StringField(
        label="",
        validators=[wtf.validators.optional()]
    )
    status = wtf.RadioField(
        label="",
        choices=[(1, 'Activo'), (0, 'No activo')],
        validators=[wtf.validators.optional()],
        coerce=int
    )
    active = wtf.RadioField(
        label="",
        choices=[(1, 'Si'), (0, 'No')],
        validators=[wtf.validators.optional()],
        coerce=int
    )
    user_email = wtf.StringField(
        label="",
        validators=[wtf.validators.optional()]
    )
    sort_by = wtf.HiddenField()
    submit_button = wtf.SubmitField(label="Aplicar")



from flask_security.forms import (
    LoginForm, RegisterForm,
    unique_user_email, email_required, email_validator
)
from wtforms import (
    StringField, PasswordField, TextField, BooleanField,
    SubmitField, validators
)
from wtforms.validators import (
    InputRequired, Required
)


_default_field_labels = {
    'username_login': 'Username ou Email',
    'username_register': 'Username/Login',
    'password': 'Senha',
    'remember_me': 'Memorizar',
    'login': 'Entrar',
    'first_name': 'Primeiro Nome',
    'last_name': 'Último Nome',
    'email': 'E-mail',
    'password': 'Nova Senha',
    'password_repeat': 'Repita a Nova Senha',
    'submit_register': 'Cadastrar'
}

def get_form_field_label(key):
    return _default_field_labels.get(key, '')

class ExtendedLoginForm(LoginForm):
    email = StringField(
        get_form_field_label('username_login'),
        [InputRequired()]
    )
    password = PasswordField(
        get_form_field_label('password'),
        [InputRequired()]
    )
    remember = BooleanField(
        get_form_field_label('remember_me'),
    )
    submit = SubmitField(
        get_form_field_label('login'),
    )

class ExtendedRegisterForm(RegisterForm):
    username = StringField(
        get_form_field_label('username_register'),
        [InputRequired()]
    )
    first_name = TextField(
        get_form_field_label('first_name'),
        [Required()]
    )
    last_name = TextField(
        get_form_field_label('last_name'),
        [Required()]
    )
    email = StringField(
        get_form_field_label('email'),
        validators=[
            validators.Length(
                  min=6, max=255,
                  message='E-mail deve ter entre 6 e 255 caracteres'
            ),
            email_required, email_validator, unique_user_email
        ]
    )
    password = PasswordField(
        'Nova Senha',
        [
            validators.DataRequired(),
            validators.Length(
                  min=6, max=50,
                  message='Senha deve ter entre 6 e 50 caracteres'
            ),
            validators.EqualTo('password_confirm', message='Senhas não são iguais')
        ]
    )
    password_confirm = PasswordField(
        'Repita a Nova Senha'
    )
    submit = SubmitField(
        get_form_field_label('submit_register')
    )


# -*- coding: utf-8 -*-
#!flask/bin/python

# pip install -r requirements.txt

import os
from flask import (Flask, url_for, render_template,
    abort, redirect
)
from flask_sqlalchemy import SQLAlchemy
from flask_security import (Security, SQLAlchemyUserDatastore,
    UserMixin, RoleMixin, login_required
)
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib import sqla

def create_app():
    # The template files will be stored in the [templates] directory
    app = Flask(__name__, template_folder="templates")
    app.debug = True
    app.config.from_pyfile('config.py')
    return app

# Construct an instance of Flask class for our webapp
app = create_app()
# Create database connection object
db = SQLAlchemy(app)

# --------------------------------
# FLASK-SECURITY MODELS
# --------------------------------
perfis_usuarios = db.Table(
    'perfil_usuario',
    db.Column('usuario_id', db.Integer(), db.ForeignKey('usuario.id')),
    db.Column('perfil_id', db.Integer(), db.ForeignKey('perfil.id'))
)

class Perfil(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    descricao = db.Column(db.String(255))

    def __str__(self):
        return self.name

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    username = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Perfil',
                            secondary=perfis_usuarios,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

# --------------------------------
# FORMS
# --------------------------------
import forms

# --------------------------------
# Setup Flask-Security
# --------------------------------
user_datastore = SQLAlchemyUserDatastore(db, Usuario, Perfil)
security = Security(app, user_datastore,
                    login_form=forms.ExtendedLoginForm,
                    register_form=forms.ExtendedRegisterForm)

# --------------------------------
# MODELS
# --------------------------------
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    desc = db.Column(db.String(50))

    def __str__(self):
        return self.desc

# --------------------------------
# MODEL VIEW CLASSES
# --------------------------------
from model_views import (
    CarAdminView, CarUserView, MyModelView
)

# --------------------------------
# FLASK VIEWS / ROUTES
# --------------------------------
@app.route('/')
def index():
    #return render_template('index.html')
    return redirect("/admin")

# --------------------------------
# CREATE FLASK ADMIN
# --------------------------------
admin = flask_admin.Admin(
    app,
    '',
    base_template='my_master.html',
    template_mode='bootstrap3',
)
admin.add_view(CarAdminView(Car, db.session))
admin.add_view(MyModelView(Perfil, db.session))
admin.add_view(MyModelView(Usuario, db.session))

# --------------------------------
# define a context processor for merging flask-admin's template context
#   into the flask-security views.
# --------------------------------
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
)

# --------------------------------
# Populate a small db with some example entries.
# --------------------------------
def build_sample_db():
    import string
    import random

    db.drop_all()
    db.create_all()

    with app.app_context():
        perfil_user = Perfil(name='usuario')
        perfil_super_user = Perfil(name='superusuario')
        db.session.add(perfil_user)
        db.session.add(perfil_super_user)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            username='admin',
            email='admin@test.com',
            password=encrypt_password('admin'),
            roles=[perfil_user, perfil_super_user]
        )

        first_names = [
            'Harry', 'Amelia', 'Oliver', 'Jack'
        ]
        last_names = [
            'Brown', 'Smith', 'Patel', 'Jones'
        ]

        for i in range(len(first_names)):
            tmp_email = "{}.{}@test.com".format(first_names[i].lower(),
                                                last_names[i].lower())
            tmp_pass = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(10))
            user_datastore.create_user(
                first_name=first_names[i],
                last_name=last_names[i],
                username=first_names[i].lower(),
                email=tmp_email,
                password=encrypt_password(tmp_pass),
                roles=[perfil_user, ]
            )
        db.session.commit()
    return

# --------------------------------
# MAIN APP
# --------------------------------
if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = os.path.realpath(os.path.dirname(__file__))
    database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()
    # Start app
    app_port = int(os.environ.get('PORT', 5000))
    app_host='0.0.0.0'
    app.run(host=app_host, port=app_port)


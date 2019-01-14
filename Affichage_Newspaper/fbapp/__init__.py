from flask import Flask

from .views import app
from . import models

# Connect sqlalchemy to app
models.db.init_app(app)

@app.cli.command('init_db')
def init_db():
    models.init_db()
    models.init_db_login()
    models.init_db_votes()

@app.cli.command('init_db_login')
def init_db_login():
    models.init_db_login()

@app.cli.command('init_db_votes')
def init_db_votes():
    models.init_db_votes()

from flask import Flask

from .views import app
from . import models

# Connect sqlalchemy to app
models.db.init_app(app)

@app.cli.command('init_db') # FLASK_APP=run.py flask init_db
def init_db():
    """
    Create/Re-initialize the whole database
    """
    models.init_db()
    models.init_db_login()
    models.init_db_votes()

@app.cli.command('init_db_login')  # FLASK_APP=run.py flask init_db_login
def init_db_login():
    """
    Create/Re-initialize the Users table
    """
    models.init_db_login()

@app.cli.command('init_db_votes')  # FLASK_APP=run.py flask init_db_votes
def init_db_votes():
    """
    Create/Re-initialize the Votes table
    """
    models.init_db_votes()

#!/Users/clementgrisi/Document2/imi/tdlog/projet/TDlog/env/bin/python3

import os

SECRET_KEY = "-0x7<dc'E/y[xd}Q$zlby?S"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

"""
This document generate the Database Entity Relation Diagram
"""

import os
from eralchemy import render_er
# Draw from SQLAlchemy base
render_er(Base, 'erd_from_sqlalchemy.png')

# Draw from database
render_er(os.environ.get('DB_CONNECTION_STRING'), 'erd_from_sqlite.png')

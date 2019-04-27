"""
This document generate the Database Entity Relation Diagram
"""

import os
from eralchemy import render_er

# Draw from database
render_er(os.environ.get('DB_CONNECTION_STRING'), 'diagram.png')

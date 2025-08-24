import sys
import logging
import os
from app import app as application  # Import your Flask app instance

sys.path.insert(0, '/home/SomePiGuy/PyCharmProjects/lennoncrow_com')

# Activate virtual environment
activate_this = '/home/SomePiGuy/PyCharmProjects/lennoncrow_com/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# __init__.py Runs when the package loads

# Creating an application object 
from flask import Flask

app = Flask(__name__)
from app import views
# Importing the views modules
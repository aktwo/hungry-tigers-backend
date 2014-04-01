import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def frontend():
    return "Sorry, no email yet!"

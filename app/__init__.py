from flask import Flask, jsonify
from flask import request
from flask_bootstrap import Bootstrap
from app.repository import Repository




##
## *global variables*
##
app = Flask(__name__)
bootstrap = Bootstrap(app)
repo = Repository()



##
## *load routes*
##
from app import routes_web
from app import routes_api

from flask import Flask, request

myapp = Flask(__name__)

from app import views

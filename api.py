from flask import request, render_template, Blueprint, abort
from config import config

api = Blueprint('api', __name__)


@api.route('/this')
def this():
    return '<p> This is my route </p>'

from flask import Blueprint

tdd_blueprint = Blueprint('tdd', __name__, url_prefix='/tdd', template_folder='templates')

from . import models, views  # noqa
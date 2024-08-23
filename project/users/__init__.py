from flask import Blueprint

users_blueprint = Blueprint("users", __name__, url_prefix="/users", template_folder="templates")

from . import events, models, tasks, views  # noqa
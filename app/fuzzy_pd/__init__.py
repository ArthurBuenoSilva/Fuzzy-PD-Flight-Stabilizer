from flask import Blueprint

bp = Blueprint("fuzzy_pd", __name__)

from app.fuzzy_pd import routes

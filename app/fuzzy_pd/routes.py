from flask import render_template

from app.fuzzy_pd import bp


@bp.route('/')
def index():
    return render_template("base.html")
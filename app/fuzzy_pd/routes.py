from flask import render_template

from app.extensions import socketio
from app.fuzzy_pd import bp
from app.fuzzy_pd.controller import controller


@bp.route("/")
def index():
    return render_template("base.html")


@socketio.on("go_to")
def go_to(set_point):
    controller.go_to(float(set_point))


@socketio.on("rth")
def rth():
    controller.return_to_home()

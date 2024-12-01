from app.extensions import socketio
from app.fuzzy_pd.fuzzy import Fuzzy


class Controller:
    def __init__(self):
        self._current_height: float = 0

    def go_to(self, set_point):
        result = Fuzzy(self._current_height).defuzzification(set_point)
        self._current_height = result.get("current_height", 0)
        socketio.emit("result", result)

    def return_to_home(self):
        result = Fuzzy(self._current_height).defuzzification(0)
        self._current_height = result.get("current_height", 0)
        socketio.emit("result", result)


controller = Controller()

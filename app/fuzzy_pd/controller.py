class Controller:
    def __init__(self):
        self._set_point: float = 0
        self._current_height: float = 0
        self._fa: float = 1
        self._p_mode: float = 3

    @property
    def set_point(self):
        return self._set_point

    @set_point.setter
    def set_point(self, value):
        self._set_point = value

    @property
    def current_height(self):
        return self._current_height

    @current_height.setter
    def current_height(self, value):
        self._current_height = value

    @property
    def fa(self):
        return self._fa

    @fa.setter
    def fa(self, value):
        self._fa = value

    @property
    def p_mode(self):
        return self._p_mode

    @p_mode.setter
    def p_mode(self, value):
        self._p_mode = value

    def calculate(self):
        pass

    def return_to_home(self):
        pass


controller = Controller()

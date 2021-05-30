from kivy.core.window import Window
from kivy.graphics import Rectangle, Color


class Bear:
    def __init__(self, position):
        self._position = position
        if self._position == 0:
            y = Window.height
        else:
            y = Window.height - int(Window.height / 5 * self._position)
        middle = int(Window.width / 2) - int(int(50 * self._position) / 2)
        self._pos = (middle, y)
        self._size = (int(50 * self._position), int(100 * self._position))
        self._alpha = (self._position * 2) / 10
        self.color = Color(rgba=(1, 1, 1, self._alpha))
        self._instruction = Rectangle(
            pos=self._pos,
            size=self._size,
            source='assets/bear.png'
        )

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        self._instruction.pos = self._pos

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._instruction.size = self._size

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value
        self.color.a = self._alpha

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        if self._position == 0:
            y = Window.height
        else:
            y = Window.height - int(Window.height / 5 * self._position)
        middle = int(Window.width / 2) - int(int(50 * self._position) / 2)
        self.pos = (middle, y)
        self.size = (int(50 * self._position), int(100 * self._position))
        self.alpha = (self._position * 2) / 10

    @property
    def instruction(self):
        return self._instruction

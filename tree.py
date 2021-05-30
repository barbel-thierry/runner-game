from kivy.graphics import Rectangle, Color


class Tree:
    def __init__(self, pos, size, alpha=1):
        self._pos = pos
        self._size = size
        self._alpha = alpha
        self._source = 'assets/tree.png'
        self.color = Color(rgba=(1, 1, 1, self._alpha))
        self._instruction = Rectangle(
            pos=self._pos,
            size=self._size,
            source=self._source
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

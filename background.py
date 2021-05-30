from kivy.graphics import Rectangle


class Background:
    def __init__(self, pos, size, vertical=False, horizontal=False):
        self._pos = pos
        self._size = size
        self._source = 'assets/ground.jpg'
        self._instruction = Rectangle(
            pos=self._pos,
            size=self._size,
            source=self._source
        )
        if vertical:
            self._instruction.texture.flip_vertical()
        if horizontal:
            self._instruction.texture.flip_horizontal()

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

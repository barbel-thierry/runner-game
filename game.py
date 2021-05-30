from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color
from kivy.uix import label
from kivy.uix.label import Label
from kivy.uix.widget import Widget

import background
import bear
import trees


class Screen(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._pressed_keys = set()
        self._pace = 20
        self.trees = []
        self._tree_size = (400, 800)
        self._score = 0
        self._score_label = label.CoreLabel(text='Score: ' + str(self._score), font_size=20)
        self._score_label.refresh()

        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        with self.canvas.before:
            size = (Window.width + (self._pace * 2), Window.height + (self._pace * 2))
            self._upper_left = background.Background(
                pos=((Window.width / 2) - size[0], 0),
                size=size,
                horizontal=True
            )
            self._upper_right = background.Background(
                pos=(Window.width / 2, 0),
                size=size,
                vertical=True,
                horizontal=True
            )
            self._lower_left = background.Background(
                pos=((Window.width / 2) - size[0], -size[1]),
                size=size,
                horizontal=True
            )
            self._lower_right = background.Background(
                pos=(Window.width / 2, -size[1]),
                size=size
            )
        with self.canvas:
            self._score_instruction = Rectangle(
                texture=self._score_label.texture,
                pos=(0, Window.height - 30),
                size=self._score_label.texture.size
            )
            self._bear = bear.Bear(0)

        self._move = Clock.schedule_interval(self._move_from_pace, 1 / 60)

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self._pressed_keys.add(keycode[1])

    def _on_key_up(self, keyboard, keycode):
        if keycode[1] in self._pressed_keys:
            self._pressed_keys.remove(keycode[1])

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self._score_label.text = "Score: " + str(value)
        self._score_label.refresh()
        self._score_instruction.texture = self._score_label.texture
        self._score_instruction.size = self._score_label.texture.size

    def _move_from_pace(self, dt):
        with self.canvas:
            if 'down' in self._pressed_keys:
                if self._deal_with_bear(self._pace * dt):
                    self._move_down()
            if 'left' in self._pressed_keys:
                trees.move_laterally(self.trees, self._pace)
                self._move_laterally(self._pace)
            if 'right' in self._pressed_keys:
                trees.move_laterally(self.trees, -self._pace)
                self._move_laterally(-self._pace)

    def _deal_with_bear(self, pace):
        if self._bear.position > 5:
            self._lost()
        if trees.has_collide(self.trees):
            if self._bear.position < 5:
                self.canvas.remove(self._bear.instruction)
                self._bear.position += pace
                self.canvas.add(self._bear.instruction)
            return False
        else:
            if self._bear.position > 0:
                self._bear.position -= pace
            return True

    def _move_down(self):
        trees.move_backward(self.trees, self._tree_size, self._pace)
        self._increment_score()

        (upper_left_x, upper_left_y) = self._upper_left.pos
        upper_left_y += self._pace
        if upper_left_y > Window.height:
            upper_left_y = -(Window.height + (self._pace * 2))
        self._upper_left.pos = (upper_left_x, upper_left_y)

        (upper_right_x, upper_right_y) = self._upper_right.pos
        upper_right_y += self._pace
        if upper_right_y > Window.height:
            upper_right_y = -(Window.height + (self._pace * 2))
        self._upper_right.pos = (upper_right_x, upper_right_y)

        (lower_left_x, lower_left_y) = self._lower_left.pos
        lower_left_y += self._pace
        if lower_left_y > Window.height:
            lower_left_y = -(Window.height + (self._pace * 2))
        self._lower_left.pos = (lower_left_x, lower_left_y)

        (lower_right_x, lower_right_y) = self._lower_right.pos
        lower_right_y += self._pace
        if lower_right_y > Window.height:
            lower_right_y = -(Window.height + (self._pace * 2))
        self._lower_right.pos = (lower_right_x, lower_right_y)

    def _move_laterally(self, pace):
        (upper_left_x, upper_left_y) = self._upper_left.pos
        upper_left_x += pace
        if upper_left_x > Window.width:
            upper_left_x = -(Window.width + pace)
        if upper_left_x < -self._upper_left.size[0]:
            upper_left_x = Window.width + pace
        self._upper_left.pos = (upper_left_x, upper_left_y)

        (upper_right_x, upper_right_y) = self._upper_right.pos
        upper_right_x += pace
        if upper_right_x > Window.width:
            upper_right_x = -(Window.width + pace)
        if upper_right_x < -self._upper_left.size[0]:
            upper_right_x = Window.width + pace
        self._upper_right.pos = (upper_right_x, upper_right_y)

        (lower_left_x, lower_left_y) = self._lower_left.pos
        lower_left_x += pace
        if lower_left_x > Window.width:
            lower_left_x = -(Window.width + pace)
        if lower_left_x < -self._upper_left.size[0]:
            lower_left_x = Window.width + pace
        self._lower_left.pos = (lower_left_x, lower_left_y)

        (lower_right_x, lower_right_y) = self._lower_right.pos
        lower_right_x += pace
        if lower_right_x > Window.width:
            lower_right_x = -(Window.width + pace)
        if lower_right_x < -self._upper_left.size[0]:
            lower_right_x = Window.width + pace
        self._lower_right.pos = (lower_right_x, lower_right_y)

    def _increment_score(self):
        self.score += 1

    def _lost(self):
        self._move.cancel()

        with self.canvas:
            text = "The Big Bear caught you...\n"
            text += "But you managed to score " + str(self._score) + " points!!\n\n"
            text += "Press `y` if you want to play again."

            Label(
                pos=((Window.width - 100) / 2, Window.height / 2),
                size=(100, 30),
                text=text
            )

            self._restart = Clock.schedule_interval(self._on_endgame, 0)

    def _on_endgame(self, dt):
        if 'y' in self._pressed_keys:
            self._restart.cancel()
            self.canvas.clear()
            self.__init__()

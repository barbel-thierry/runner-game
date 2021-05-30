from kivy.app import App

import game


class NURApp(App):
    def build(self):
        return game.Screen()


if __name__ == '__main__':
    NURApp().run()

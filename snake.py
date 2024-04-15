from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import random


class SnakeGame(Widget):
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake = [(0, 0)]
        self.food = self.generate_food()
        self.direction = (1, 0)
        self.score = 0
        self.update_interval = 0.1
        self.bind(size=self.resize)
        self.bind(pos=self.redraw)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.direction = (0, 1)
        elif keycode[1] == 'down':
            self.direction = (0, -1)
        elif keycode[1] == 'left':
            self.direction = (-1, 0)
        elif keycode[1] == 'right':
            self.direction = (1, 0)

    def resize(self, *args):
        self.redraw()

    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            for segment in self.snake:
                Color(0, 1, 0)
                Rectangle(pos=(self.pos[0] + segment[0] * 10, self.pos[1] + segment[1] * 10), size=(10, 10))
            Color(1, 0, 0)
            Rectangle(pos=(self.pos[0] + self.food[0] * 10, self.pos[1] + self.food[1] * 10), size=(10, 10))

    def generate_food(self):
        while True:
            x = random.randint(0, int((self.width - 10) / 10))
            y = random.randint(0, int((self.height - 10) / 10))
            if (x, y) not in self.snake:
                return x, y

    def update(self, dt):
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        if (
            0 <= new_head[0] < int(self.width / 10)
            and 0 <= new_head[1] < int(self.height / 10)
            and new_head not in self.snake[1:]
        ):
            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.food = self.generate_food()
                self.score += 1
            else:
                self.snake.pop()
        else:
            self.snake = [(0, 0)]
            self.direction = (1, 0)
            self.score = 0
        self.redraw()

    def on_touch_down(self, touch):
        pass


class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        Clock.schedule_interval(game.update, game.update_interval)
        return game


if __name__ == '__main__':
    SnakeApp().run()
from abc import ABC, abstractmethod
import arcade

class BaseBrush(ABC):
    def __init__(self, sprite_path=None):
        self.active = False
        self.sprite = None
        if sprite_path is not None:
            self.sprite = arcade.Sprite(sprite_path)


    @abstractmethod
    def paint(self, palette, index):
        pass

    def draw(self, x, y):
        if self.sprite is not None:
            self.sprite.center_x = x
            self.sprite.center_y = y
            self.sprite.draw()

class BasicBrush(BaseBrush):
    def __init__(self):
        super().__init__('icons/pencil-sm.png')

    def paint(self, palette, index):
        palette[index] = True


class EraserBrush(BaseBrush):
    def __init__(self):
        super().__init__('icons/eraser-sm.png')

    def paint(self, palette, index):
        palette[index] = False

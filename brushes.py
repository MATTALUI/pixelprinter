from abc import ABC, abstractmethod

class BaseBrush(ABC):
    def __init__(self):
        self.active = False

    @abstractmethod
    def paint(self, palette, index):
        pass

    @abstractmethod
    def draw(self, x, y):
        pass

class BasicBrush(BaseBrush):
    def paint(self, palette, index):
        palette[index] = True

    def draw(self, x, y):
        pass

class EraserBrush(BaseBrush):
    def paint(self, palette, index):
        palette[index] = False

    def draw(self, x, y):
        pass

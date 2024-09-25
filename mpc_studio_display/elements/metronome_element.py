from ..display import Element
from ..graphics import PngDrawing


class MetronomeElement(Element):
    def __init__(self, x, y):
        super().__init__("metronome", x, y, 19, 9)
        self._enabled = False

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self.render()

    def render(self):
        if self._enabled:
            PngDrawing.draw_rectangle(self, self.x, self.y, self.width, self.height, (255,255,255))
            PngDrawing.draw_circle(self, self.x + 5, self.y + 4, 2, (0,0,0))
            PngDrawing.draw_circle(self, self.x + 12, self.y + 4, 2, (0, 0, 0))
        else:
            PngDrawing.draw_rectangle_outline(self, (self.x, self.y), (self.x + self.width - 2, self.y + self.height - 1), (255,255,255))
            PngDrawing.draw_circle(self, self.x + 5, self.y + 4, 2, (255, 255, 255))
            PngDrawing.draw_circle(self, self.x + 12, self.y + 4, 2, (255, 255, 255))
        super().render()
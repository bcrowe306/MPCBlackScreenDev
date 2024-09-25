from ..display import Element
from ..graphics import PngDrawing

class TextElement(Element):
    def __init__(self, name, value, x, y, width, height, scale=1, selected = False) -> None:
        super().__init__(name, x, y, width, height)
        self._text = value
        self.scale = scale
        self._selected = selected
        self._enabled = True

    @property
    def enabled(self):
        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        self._enabled = value
        self.render()

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    def render_selected(self):
        if self._enabled:
            font_height = 7 * self.scale
            center_start_y = self.y + ((self.height - font_height) // 2)
            PngDrawing.draw_rectangle(self, self.x, self.y, self.width, self.height, (255,255,255))
            PngDrawing.draw_text(self, self._text, self.x+1, center_start_y, scale=self.scale, color=(0,0,0))

    def render_unselected(self):
        if self._enabled:
            font_height = 7 * self.scale
            center_start_y = self.y + ((self.height - font_height) // 2)
            PngDrawing.draw_rectangle(self, self.x, self.y, self.width, self.height, (0,0,0))
            PngDrawing.draw_text(self, self._text, self.x+1, center_start_y, scale=self.scale, color=(255,255,255))

    def render(self):
        if self._selected:
            self.render_selected()
        else:
            self.render_unselected()
        super().render()

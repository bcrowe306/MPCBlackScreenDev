from ..display import Element
from ..graphics import PngDrawing

class MeterElement(Element):
    def __init__(self, x, y, width, height, scale=1, selected=False) -> None:
        super().__init__(x, y, width, height)
        self.scale = scale
        self._value = 0
        self._selected = selected

    @property
    def left_value(self):
        return self._left_value

    @left_value.setter
    def left_value(self, value):
        self._left_value = value
        self.render()

    @property
    def right_value(self):
        return self._right_value
    
    @right_value.setter
    def right_value(self, value):
        self._right_value = value
        self.render()

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value
        self.render()

    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        self._volume = value
        self.render()

    def render(self):
        return super().render()
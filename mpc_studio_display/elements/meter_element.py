from ..display import Element
from ..graphics import PngDrawing, Icons_5x5

class MeterElement(Element):
    def __init__(self, x, y, width, height) -> None:
        super().__init__("meter_element", x, y, width, height)
        self._left_meter = .5
        self._right_meter = .5
        self._volume = .5

    @property
    def left_meter(self):
        return self._left_meter
    
    @left_meter.setter
    def left_meter(self, value):
        self._left_meter = value
        self.render()

    @property
    def right_meter(self):
        return self._right_meter
    
    @right_meter.setter
    def right_meter(self, value):
        self._right_meter = value
        self.render()

    @property
    def volume(self):
        return self._volume
    
    @volume.setter
    def volume(self, value):
        self._volume = value
        self.render()

    def set_meters(self, left, right):
        self._left_meter = left
        self._right_meter = right
        self.render()

    def set_meters_from_midi(self, left, right):
        self._left_meter = left / 127
        self._right_meter = right / 127
        self.render()

    def set_volume_from_midi(self, value):
        self._volume = value / 127
        self.render()

    def set_all_from_midi(self, left, right, volume):
        self._left_meter = left / 127
        self._right_meter = right / 127
        self._volume = volume / 127
        self.render()

    def set_all(self, left, right, volume):
        self._left_meter = left
        self._right_meter = right
        self._volume = volume
        self.render()

    def __draw_meters(self):
        meter_width = (self.width // 3) - 1
        meter_height = self.height
        meter_x = meter_width
        meter_y = 0

        # Draw left meter
        PngDrawing.draw_vertical_meter(
            self, self._left_meter, meter_x, meter_y, meter_width, meter_height
        )
        # Draw right meter
        PngDrawing.draw_vertical_meter(
            self,
            self._right_meter,
            meter_x + meter_width,
            meter_y,
            meter_width,
            meter_height,
        )

    def __draw_volume(self):
        volume_height = self.height
        volume_y = volume_height - int(self._volume * volume_height) - 2
        PngDrawing.draw_icon(self, Icons_5x5.play, 0, volume_y, color=(255, 255, 255))

    def render(self):
        self.clear()
        self.__draw_meters()
        self.__draw_volume()
        super().render()

from ..display import Element
from ..graphics import PngDrawing

class ClipSlotStates:
    EMPTY = 0
    STOPPED = 1
    TRIGGERED = 2
    PLAYING = 3
    RECORDING = 4
    STOPPING = 5

class ClipSlotElement(Element):
    def __init__(self, text, x, y, width, height, scale=1, selected=False) -> None:
        super().__init__(x, y, width, height)
        self._text = text
        self.scale = scale
        self._state = selected
        self.render_mapping = {
            ClipSlotStates.EMPTY: self.render_empty,
            ClipSlotStates.STOPPED: self.render_stopped,
            ClipSlotStates.TRIGGERED: self.render_triggered,
            ClipSlotStates.PLAYING: self.render_playing,
            ClipSlotStates.RECORDING: self.render_recording,
            ClipSlotStates.STOPPING: self.render_stopping,
        }
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    def render_selected(self):
        font_height = 7 * self.scale
        center_start_y = self.y + ((self.height - font_height) // 2)
        PngDrawing.draw_rectangle(
            self, self.x, self.y, self.width, self.height, (255, 255, 255)
        )
        PngDrawing.draw_text(
            self, self._text, self.x, center_start_y, scale=self.scale, color=(0, 0, 0)
        )

    def render_unselected(self):
        font_height = 7 * self.scale
        center_start_y = self.y + ((self.height - font_height) // 2)
        PngDrawing.draw_rectangle(
            self, self.x, self.y, self.width, self.height, (0, 0, 0)
        )
        PngDrawing.draw_text(
            self,
            self._text,
            self.x,
            center_start_y,
            scale=self.scale,
            color=(255, 255, 255),
        )

    def render_empty(self):
        pass

    def render_stopped(self):
        pass

    def render_triggered(self):
        pass

    def render_playing(self):
        pass

    def render_recording(self):
        pass

    def render_stopping(self):
        pass


    def render(self):
        state_renderer = self.render_mapping.get(self._state, self.render_empty)
        if state_renderer and callable(state_renderer):
            state_renderer()
        super().render()

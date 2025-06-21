from ..display import Element
from ..graphics import PngDrawing, Icons_5x5

class ClipSlotStates:
    EMPTY = 0
    STOPPED = 1
    TRIGGERED = 2
    PLAYING = 3
    RECORDING = 4
    STOPPING = 5

class ClipSlotElement(Element):
    class States:
        EMPTY = 0
        STOPPED = 1
        TRIGGERED = 2
        PLAYING = 3
        RECORDING = 4
        STOPPING = 5

    def __init__(self, text, x, y, width, height, scale=1, selected=False, last=False) -> None:
        super().__init__(text, x, y, width, height)
        self._text = text
        self.scale = scale
        self.last = last
        self._selected = False
        self.render_mapping = {
            ClipSlotStates.EMPTY: self.render_empty,
            ClipSlotStates.STOPPED: self.render_stopped,
            ClipSlotStates.TRIGGERED: self.render_triggered,
            ClipSlotStates.PLAYING: self.render_playing,
            ClipSlotStates.RECORDING: self.render_recording,
            ClipSlotStates.STOPPING: self.render_stopping,
        }
        self._state = ClipSlotElement.States.STOPPED

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        self._selected = value
        self.render()
    
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

    def render_selected(self, empty=False):
        if empty:
            color = (255, 255, 255)
        else:
            color = (0, 0, 0)
        y = 10
        PngDrawing.draw_line(self, (10, y), (50, y), color=color)

    def __draw_stop_icon(self, empty=False):
        if not empty:
            PngDrawing.draw_icon(
                self,
                Icons_5x5.stop,
                self.x + 3,
                self.y + 3,
                color=(0, 0, 0),
                background_color=(255, 255, 255),
            )
        else:
            PngDrawing.draw_icon(self, Icons_5x5.stop, self.x + 3, self.y + 3 , color=(255, 255, 255), background_color=(0, 0, 0))

    def render_empty(self):
        pass

    def render_stopped(self):
        PngDrawing.draw_rectangle(self, self.x, self.y, self.width, self.height, color=(255,255,255))
        self.__draw_stop_icon(empty=False)
        PngDrawing.draw_text(self, self._text, self.x + 12, self.y + 2, scale=self.scale, color=(0, 0, 0))
        if not self.last:
            PngDrawing.draw_line(self, (0, 12), (59, 12), (255, 255, 255))
        if self.selected:
            self.render_selected()

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

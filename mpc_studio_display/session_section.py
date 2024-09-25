from .graphics import PngDrawing
from .elements.text_element import TextElement
from .display import Element

class TrackStates:
    NONE = 0
    EMPTY = 1
    SELECTED = 2


class TrackElement(Element):
    def __init__(self, name, x, y, state=TrackStates.EMPTY) -> None:
        super().__init__(name, x, y, 60, 96)
        self._state = state
        self._track_name = name
        self.track_name_element = TextElement("track_name_element", self._track_name, self.x_pos + 2, self.y_pos, 59, 13, selected=False)

    def render_none(self):
        self.track_name_element.enabled = False

    def render_empty(self):
        PngDrawing.draw_line(self, (59, 0), (59, 96), (255, 255, 255))
        PngDrawing.draw_line(self, (0, 13), (60, 13), (255, 255, 255))
        # Draw footer horizontal line
        PngDrawing.draw_line(self, (0, 71), (59, 71), (255, 255, 255))
        PngDrawing.draw_rectangle(self, 28, 74, 5, 5, (255, 255, 255))

    def render_selected(self):
        self.track_name_element.selected = True
        self.track_name_element.enabled = True
        PngDrawing.draw_line(self, (59, 0), (59, 96), (255, 255, 255))
        PngDrawing.draw_line(self, (0, 13), (60, 13), (255, 255, 255))
        # Draw footer horizontal line
        PngDrawing.draw_line(self, (0, 71), (59, 71), (255, 255, 255))
        PngDrawing.draw_rectangle(self, 28, 74, 5, 5, (255, 255, 255))

    @property
    def track_name(self):
        return self._track_name

    @track_name.setter
    def track_name(self, value):
        self._track_name = value
        self.render()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        self.render()

    def render(self):
        render_mapping = {
            TrackStates.NONE: self.render_none,
            TrackStates.EMPTY: self.render_empty,
            TrackStates.SELECTED: self.render_selected,
        }
        renderer = render_mapping[self._state]
        renderer()
        super().render()

class SessionSection(Element):
    def __init__(self) -> None:
        super().__init__("session_section", 0, 14, 240, 96)
        self.track_1 = TrackElement("track_1", 0, 13, state=TrackStates.EMPTY)
        self.track_2 = TrackElement("track_2", 60, 13, state=TrackStates.EMPTY)
        self.track_3 = TrackElement("track_3", 120, 13, state=TrackStates.EMPTY)
        self.track_4 = TrackElement("track_4", 180, 13, state=TrackStates.EMPTY)

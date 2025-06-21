from .graphics import PngDrawing, Icons_5x5
from .elements.text_element import TextElement
from .elements.clip_slot_element import ClipSlotElement
from .elements.meter_element import MeterElement
from .display import Element

class SessionTrackElement(Element):
    class States:
        NONE = 0
        EMPTY = 1
        SELECTED = 2

    def __init__(self, name, x, y, state=1) -> None:
        super().__init__(name, x, y, 60, 96)
        self._state = state

        self._track_name = name
        self.track_name_element = TextElement("track_name_element", self._track_name, self.x_pos + 2, self.y_pos, 59, 13, selected=False)

        # Add clipslot elements
        self.clips = []
        for i in range(4):
            clip_x = self.x_pos
            clip_y = i * 14 + 28
            clip_width = 59
            clip_height = 13
            clip_name = f"clip_{i}"
            clip = ClipSlotElement(clip_name, clip_x, clip_y, clip_width, clip_height, selected=False, last=i == 3)
            self.add_element(clip)
            self.clips.append(clip)

        self.render_mapping = {
            SessionTrackElement.States.NONE: self.__render_none,
            SessionTrackElement.States.EMPTY: self.__render_empty,
            SessionTrackElement.States.SELECTED: self.__render_selected,
        }

    def select_clip(self, index):
        for i, clip in enumerate(self.clips):
            clip.selected = i == index

    def deselect_clips(self):
        for clip in self.clips:
            clip.selected = False

    def __render_none(self):
        self.clear()
        self.track_name_element.clear()
        self.deselect_clips()
        self.track_name_element.enabled = False

    def __draw_track_header(self):
        PngDrawing.draw_line(self, (59, 0), (59, 96), (255, 255, 255))
        PngDrawing.draw_line(self, (0, 13), (60, 13), (255, 255, 255))

    def __draw_track_footer(self):
        PngDrawing.draw_line(self, (0, 71), (59, 71), (255, 255, 255))
        PngDrawing.draw_rectangle(self, 28, 74, 5, 5, (255, 255, 255))

    def __render_empty(self):
        self.clear()
        self.track_name_element.selected = False
        self.deselect_clips()
        self.__draw_track_header()
        self.__draw_track_footer()

    def __render_selected(self):
        self.clear()
        self.track_name_element.clear()
        self.track_name_element.selected = True
        self.track_name_element.enabled = True
        self.__draw_track_header()
        self.__draw_track_footer()

    @property
    def track_name(self):
        return self._track_name

    @track_name.setter
    def track_name(self, value):
        self._track_name = value
        self.track_name_element.text = value
        self.render()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value != self._state:
            self._state = value
            self.render()

    def render(self):
        renderer = self.render_mapping[self._state]
        renderer()
        super().render()

class SessionSection(Element):
    def __init__(self) -> None:
        super().__init__("session_section", 0, 14, 240, 96)
        self.tracks = []
        for i in range(4):
            track = SessionTrackElement(f"track_{i+1}", i * 60, 13, state=SessionTrackElement.States.EMPTY)
            self.add_element(track)
            self.tracks.append(track)


class TrackDetailsSection(Element):
    def __init__(self) -> None:
        super().__init__("track_details_section", 241, 14, 119, 96)
        self.track_name = TextElement("track_name", "Track Name", self.x_pos, self.y_pos, 119, 12)
        self.meter_element = MeterElement(self.x_pos + 25, self.y_pos + 17, 18, 62)
        self.add_element(self.meter_element)
        self.add_element(self.track_name)

        self._mute = False
        self._solo = False
        self._arm = False
        self._pan = .5
    
    def set_pan_float(self, value):
        self._pan = value
        self.render()
    
    def set_pan_from_midi(self, value):
        self._pan = value / 127
        self.render()

    @property
    def arm(self):
        return self._arm

    @arm.setter
    def arm(self, value):
        self._arm = value
        self.render()

    @property
    def pan(self):
        return self._pan

    @pan.setter
    def pan(self, value):
        self._pan = value
        self.render()

    @property
    def mute(self):
        return self._mute

    @mute.setter
    def mute(self, value):
        self._mute = value
        self.render()

    @property
    def solo(self):
        return self._solo

    @solo.setter
    def solo(self, value):
        self._solo = value
        self.render()   

    def __draw_button(self, x, y, width, height, text, pressed=False):
        color = (0, 0, 0) if pressed else (255, 255, 255)
        background_color = (255, 255, 255) if pressed else (0, 0, 0)
        center_x = x + (width - len(text) * 5) // 2
        center_y = y + (height - 5) // 2

        if pressed:
            PngDrawing.draw_rectangle(self, x, y, width, height, background_color)
        else:
            PngDrawing.draw_rectangle_outline(
                self, (x, y), (x + width, y + height), color
            )

        PngDrawing.draw_text(self, text, center_x, center_y, color=color)

    def __draw_arm(self, x, y, width, height, pressed=False):
        circle_diameter = 3
        color = (0, 0, 0) if pressed else (255, 255, 255)
        background_color = (255, 255, 255) if pressed else (0, 0, 0)
        center_x = x + (width) // 2
        center_y = y + (height) // 2

        if pressed:
            PngDrawing.draw_rectangle(self, x, y, width, height, background_color)
        else:
            PngDrawing.draw_rectangle_outline(self, (x, y), (x + width, y +height), color)

        PngDrawing.draw_circle(self, center_x, center_y, circle_diameter, color=color)

    def render(self):
        self.clear()
        # Horizontal Line
        PngDrawing.draw_line(self, (0, 12), (122, 12), (255, 255, 255))

        # Vertical Line
        PngDrawing.draw_line(self, (45, 13), (45, 80), (255, 255, 255))
        PngDrawing.draw_knob(self, self._pan, 5, 18, 15, color=(255, 255, 255))

        self.__draw_button(5, 38, 15, 13, "M", pressed=not self._mute)
        self.__draw_button(5, 55, 15, 10, "S", pressed=self._solo)
        self.__draw_arm(5, 69, 15, 10, pressed=self._arm)



        self.__draw_button(50, 16, 65, 10, "In Port", pressed=False)
        self.__draw_button(50, 29, 65, 10, "In Chann", pressed=False)
        self.__draw_button(50, 42, 16, 10, "In", pressed=False)
        self.__draw_button(68, 42, 26, 10, "Auto", pressed=False)
        self.__draw_button(96, 42, 19, 10, "Off", pressed=False)
        self.__draw_button(50, 55, 65, 10, "Out Port", pressed=False)
        self.__draw_button(50, 68, 65, 10, "Out Chann", pressed=False)

        super().render()

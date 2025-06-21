from .util import clamp, message_length, msblsb
from .graphics import PngDrawing, ImageSection, Icons_5x5
DISPLAY_WIDTH = 360
DISPLAY_HEIGHT = 96
class Display:

    def __init__(self, send_payload ) -> None:
        self.send_payload = send_payload
        self.pages = {}
        self._current_page = None

    def initialize(self):
        for page_name in self.pages:
            page = self.pages[page_name]
            page.initialize(self.send_payload)

    def add_page(self, name, page):
        self.pages[name] = page

    def show_page(self, name):
        for page_name in self.pages:
            page = self.pages[page_name]
            if page_name != name:
                page.deactivate()
            else:
                if self._current_page == name:
                    return
                else:
                    page.activate()
                    page.render()
                    self._current_page = name


class Element(ImageSection):
    def __init__(self, name, x, y, width, height) -> None:
        super().__init__(0, 0, width, height)
        self.x_pos = x
        self.y_pos = y
        self.name = name
        self.send_payload = None
        self.active = False

    def set_activte(self, value):
        if value:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.active = True
        for attr in dir(self):
            el = getattr(self, attr)
            if isinstance(el, Element):
                el.activate()

    def deactivate(self):
        self.active = False
        for attr in dir(self):
            el = getattr(self, attr)
            if isinstance(el, Element):
                el.deactivate()

    def __encode_line(self, line):
        arr = []
        bit = 0x00
        bitmap = [0x30, 0x0C, 0x03]
        for i, pixel in enumerate(line):
            stride = i % 3
            if pixel[0] > 0:
                bit = bit | bitmap[stride]
            else:
                bit = bit | 0x00
            if stride == 2 and i > 0:
                arr.append(bit)
                bit = 0x00
        return arr

    def add_element(self, element, name=None):
        name = name if name else element.name
        setattr(self, name, element)
        return element

    def render(self):
        if self.active:
            for y, row in enumerate(self.data):
                pixels = msblsb(len(row))
                xpos = msblsb(self.x_pos)
                ypos = msblsb(self.y_pos + y)
                pixel_data = self.__encode_line(row)
                payload = pixels + xpos + ypos + tuple(pixel_data)
                self.send_payload(payload)

            # render all elements that belong to this element
            for attr in dir(self):
                el = getattr(self, attr)
                if isinstance(el, Element):
                    el.render()

    def initialize(self, send_payload):
        setattr(self, 'send_payload', send_payload) 
        for attr in dir(self):
            el = getattr(self, attr)
            if isinstance(el, Element):
                el.initialize(send_payload)

class Page(Element):
    def __init__(self, name):
        super().__init__(name, 0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

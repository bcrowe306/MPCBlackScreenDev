from mpc_studio_display.display import DISPLAY_WIDTH, Element
from mpc_studio_display.elements.text_element import TextElement
from mpc_studio_display.graphics import PngDrawing


class HeaderBarSection(Element):
    """
    A section for the title bar of the browser page.
    """
    def __init__(self, name, title, x=0, y=0, width = DISPLAY_WIDTH, height= 12):
        super().__init__(name, x, y, width, height)
        self.left_text = TextElement(f"{title}_title", title, x + 2, y + 1, 120, height - 2)
        self.center_text = TextElement(f"{title}_center", "Center Text", x + 120, y + 1, 120, height - 2)
        self.right_text = TextElement(f"{title}_right", "Right Text", x + 240, y + 1, 120, height - 2)

    def render(self):
        PngDrawing.draw_line(self, (0, self.height-1), (DISPLAY_WIDTH, self.height-1), (255, 255, 255))
        super().render()
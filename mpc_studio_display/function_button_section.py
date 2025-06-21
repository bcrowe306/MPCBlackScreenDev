from mpc_studio_display.display import DISPLAY_HEIGHT, DISPLAY_WIDTH, Element
from mpc_studio_display.elements.text_element import TextElement
from mpc_studio_display.graphics import PngDrawing


class FunctionButtonSection(Element):
    """
    A section for function buttons on the browser page.
    """
    def __init__(self, name, x=0, y=DISPLAY_HEIGHT-12, width=DISPLAY_WIDTH, height=12):
        super().__init__(name, x, y, width, height)
        # Six function buttons each 60 pixels wide and 12 pixels tall as text elements
        for i in range(6):
            button_name = f"function_button_{i+1}"
            button_text = f"F {i+1}"
            button_x = x + (i * 60) + 8
            button_y = y + 2
            button_width = 51
            button_height = height - 2
            button_element = TextElement(button_name, button_text, button_x, button_y, button_width, button_height)
            setattr(self, button_name, button_element)
            self.add_element(button_element, button_name)


    def render(self):
        PngDrawing.draw_line(self, (0, self.y), (self.width, self.y), (255, 255, 255))
        # draw vertical lines between buttons
        for i in range(1, 6):
            x_pos = i * 60
            PngDrawing.draw_line(self, (x_pos, self.y), (x_pos, self.y + self.height), (255, 255, 255))
        super().render()
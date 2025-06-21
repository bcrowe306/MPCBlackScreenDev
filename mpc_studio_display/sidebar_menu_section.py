from mpc_studio_display.display import DISPLAY_HEIGHT, Element
from mpc_studio_display.graphics import PngDrawing


class SidebarMenuSection(Element):
    """
    A section for the sidebar menu of the browser page.
    """
    def __init__(self, name, lines=6, x=0, y=0, width=60, height=DISPLAY_HEIGHT):
        super().__init__(name, x, y, width, height)
        self.__lines = lines
        self.__selected_line = 0
        self.line_texts = [f"Line {i+1}" for i in range(lines)]

    def set_line_text(self, line_index, text, selected_line_index=None):
        """
        Set the text for a specific line in the sidebar menu.
        """
        if 0 <= line_index < self.__lines:
            self.line_texts[line_index] = text
            if selected_line_index is not None:
                self.__selected_line = selected_line_index
            self.render()

    def get_line_text(self, line_index):
        """
        Get the text for a specific line in the sidebar menu.
        """
        if 0 <= line_index < self.__lines:
            return self.line_texts[line_index]
        return None

    def set_lines_text(self, texts, selected_line_index=None):
        """
        Set the text for all lines in the sidebar menu.
        """
        if len(texts) == self.__lines:
            self.line_texts = texts
            if selected_line_index is not None:
                self.__selected_line = selected_line_index
            self.render()
        else:
            raise ValueError(f"Expected {self.__lines} texts, got {len(texts)}")

    @property
    def lines(self):
        """
        Get the number of lines in the sidebar menu.
        """
        return self.__lines

    @property
    def selected_line(self):
        """
        Get the currently selected line in the sidebar menu.
        """
        return self.__selected_line

    @selected_line.setter
    def selected_line(self, line_index):
        """
        Set the currently selected line in the sidebar menu.
        """
        # clamp the line index to the valid range
        self.__selected_line = max(0, min(line_index, self.__lines - 1))
        self.render()

    def increment_selected_line(self):
        """
        Increment the currently selected line in the sidebar menu.
        """
        self.selected_line += 1

    def decrement_selected_line(self):
        """
        Decrement the currently selected line in the sidebar menu.
        """
        self.selected_line -= 1

    def render(self):
        self.clear()
        PngDrawing.draw_line(self, (self.width - 1, 0), (self.width - 1, self.height), (255, 255, 255))
        for i, text in enumerate(self.line_texts):
            text_color = (255, 255, 255)
            bg_color = (0, 0, 0)
            if i == self.__selected_line:
                text_color = (0, 0, 0)
                bg_color = (255, 255, 255)

            PngDrawing.draw_rectangle(self, 0, i * 12 , self.width - 1, 12, bg_color)
            PngDrawing.draw_text(self, text, 2, i * 12 + 2, color=text_color)
        super().render()
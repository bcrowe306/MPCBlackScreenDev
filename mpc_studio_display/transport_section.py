from .elements.metronome_element import MetronomeElement
from .elements.text_element import TextElement
from .graphics import PngDrawing
from .display import Element


class TransportSection(Element):
    def __init__(self):
        super().__init__("transport", 0, 0, 360, 13)
        self.tempo = TextElement("tempo", "120.00", 15, 0, 60, 12)
        self.time_signature = TextElement("time_signature", "4/4", 80, 0, 60, 12)
        self.metronome = MetronomeElement(145, 2)
        self.launch_quantize = TextElement("launch_quantize", "1 Bar", 205, 0, 60, 12)
        self.song_position = TextElement("song_position", "1.1.1", 265, 0, 60, 12)
        self.song_length = TextElement("song_length", "4.1.1", 330, 0, 60, 12)
        PngDrawing.draw_line(self, (0, 12), (360, 12), (255,255,255))


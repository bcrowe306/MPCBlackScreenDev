from typing import Tuple, List, BinaryIO
import zlib, math
import struct
from io import BytesIO
sin = math.sin 
cos = math.cos
rad = math.radians


font_5x7 = {
    "A": [0b01110, 0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001],
    "B": [0b11110, 0b10001, 0b11110, 0b10001, 0b10001, 0b10001, 0b11110],
    "C": [0b01110, 0b10001, 0b10000, 0b10000, 0b10000, 0b10001, 0b01110],
    "D": [0b11100, 0b10010, 0b10001, 0b10001, 0b10001, 0b10010, 0b11100],
    "E": [0b11111, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000, 0b11111],
    "F": [0b11111, 0b10000, 0b11110, 0b10000, 0b10000, 0b10000, 0b10000],
    "G": [0b01110, 0b10001, 0b10000, 0b10111, 0b10001, 0b10001, 0b01111],
    "H": [0b10001, 0b10001, 0b11111, 0b10001, 0b10001, 0b10001, 0b10001],
    "I": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b11111],
    "J": [0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b10001, 0b01110],
    "K": [0b10001, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010, 0b10001],
    "L": [0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11111],
    "M": [0b10001, 0b11011, 0b10101, 0b10101, 0b10001, 0b10001, 0b10001],
    "N": [0b10001, 0b11001, 0b10101, 0b10011, 0b10001, 0b10001, 0b10001],
    "O": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "P": [0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000, 0b10000],
    "Q": [0b01110, 0b10001, 0b10001, 0b10001, 0b10001, 0b10101, 0b01110],
    "R": [0b11110, 0b10001, 0b10001, 0b11110, 0b10010, 0b10001, 0b10001],
    "S": [0b01111, 0b10000, 0b10000, 0b01110, 0b00001, 0b00001, 0b11110],
    "T": [0b11111, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "U": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01110],
    "V": [0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "W": [0b10001, 0b10001, 0b10001, 0b10101, 0b10101, 0b11011, 0b10001],
    "X": [0b10001, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001, 0b10001],
    "Y": [0b10001, 0b10001, 0b01010, 0b00100, 0b00100, 0b00100, 0b00100],
    "Z": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b10000, 0b11111],
    "0": [0b01110, 0b10001, 0b10011, 0b10101, 0b11001, 0b10001, 0b01110],
    "1": [0b00100, 0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "2": [0b01110, 0b10001, 0b00001, 0b00110, 0b01000, 0b10000, 0b11111],
    "3": [0b11111, 0b00010, 0b00100, 0b00010, 0b00001, 0b10001, 0b01110],
    "4": [0b00010, 0b00110, 0b01010, 0b10010, 0b11111, 0b00010, 0b00010],
    "5": [0b11111, 0b10000, 0b11110, 0b00001, 0b00001, 0b10001, 0b01110],
    "6": [0b00110, 0b01000, 0b10000, 0b11110, 0b10001, 0b10001, 0b01110],
    "7": [0b11111, 0b00001, 0b00010, 0b00100, 0b01000, 0b01000, 0b01000],
    "8": [0b01110, 0b10001, 0b10001, 0b01110, 0b10001, 0b10001, 0b01110],
    "9": [0b01110, 0b10001, 0b10001, 0b01111, 0b00001, 0b00010, 0b01100],
    "a": [0b00000, 0b00000, 0b01110, 0b00001, 0b01111, 0b10001, 0b01111],
    "b": [0b10000, 0b10000, 0b11110, 0b10001, 0b10001, 0b10001, 0b11110],
    "c": [0b00000, 0b00000, 0b01110, 0b10001, 0b10000, 0b10001, 0b01110],
    "d": [0b00001, 0b00001, 0b01111, 0b10001, 0b10001, 0b10001, 0b01111],
    "e": [0b00000, 0b00000, 0b01110, 0b10001, 0b11111, 0b10000, 0b01110],
    "f": [0b00110, 0b01001, 0b01000, 0b11100, 0b01000, 0b01000, 0b01000],
    "g": [0b00000, 0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b11110],
    "h": [0b10000, 0b10000, 0b10110, 0b11001, 0b10001, 0b10001, 0b10001],
    "i": [0b00100, 0b00000, 0b01100, 0b00100, 0b00100, 0b00100, 0b01110],
    "j": [0b00010, 0b00000, 0b00110, 0b00010, 0b00010, 0b00010, 0b10010, 0b01100],
    "k": [0b10000, 0b10000, 0b10010, 0b10100, 0b11000, 0b10100, 0b10010],
    "l": [0b01100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b01110],
    "m": [0b00000, 0b00000, 0b11010, 0b10101, 0b10101, 0b10101, 0b10101],
    "n": [0b00000, 0b00000, 0b11110, 0b10001, 0b10001, 0b10001, 0b10001],
    "o": [0b00000, 0b00000, 0b01110, 0b10001, 0b10001, 0b10001, 0b01110],
    "p": [0b00000, 0b00000, 0b11110, 0b10001, 0b10001, 0b11110, 0b10000, 0b10000],
    "q": [0b00000, 0b00000, 0b01111, 0b10001, 0b10001, 0b01111, 0b00001, 0b00001],
    "r": [0b00000, 0b00000, 0b10110, 0b11001, 0b10000, 0b10000, 0b10000],
    "s": [0b00000, 0b00000, 0b01110, 0b10000, 0b01110, 0b00001, 0b11110],
    "t": [0b01000, 0b01000, 0b11100, 0b01000, 0b01000, 0b01001, 0b00110],
    "u": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b10011, 0b01101],
    "v": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b01010, 0b00100],
    "w": [0b00000, 0b00000, 0b10001, 0b10001, 0b10101, 0b10101, 0b01010],
    "x": [0b00000, 0b00000, 0b10001, 0b01010, 0b00100, 0b01010, 0b10001],
    "y": [0b00000, 0b00000, 0b10001, 0b10001, 0b10001, 0b01111, 0b00001, 0b01110],
    "z": [0b00000, 0b00000, 0b11111, 0b00010, 0b00100, 0b01000, 0b11111],
    ":": [0b00100, 0b00100, 0b00000, 0b00000, 0b00000, 0b00100, 0b00100],
    "_": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111],
    "-": [0b00000, 0b00000, 0b00000, 0b11111, 0b00000, 0b00000, 0b00000],
    "+": [0b00000, 0b00100, 0b00100, 0b11111, 0b00100, 0b00100, 0b00000],
    "*": [0b00000, 0b00000, 0b00000, 0b00100, 0b00000, 0b00000, 0b00000],
    ".": [0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00110, 0b00000],
    "[": [0b11100, 0b10000, 0b10000, 0b10000, 0b10000, 0b10000, 0b11100],
    "]": [0b00111, 0b00001, 0b00001, 0b00001, 0b00001, 0b00001, 0b00111],
    "|": [0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100, 0b00100],
    "/": [0b00001, 0b00010, 0b01000, 0b00100, 0b01000, 0b01000, 0b10000],
}


class Icons_5x5:
    drums = [0b11011, 0b11011, 0b00000, 0b11011, 0b11011]
    audio = [0b01000, 0b01110, 0b11111, 0b01110, 0b01000]
    midi = [0b11111, 0b10101, 0b10101, 0b10001, 0b11111]
    instrument = [0b11111, 0b10001, 0b11111, 0b11111, 0b11111]
    group = [0b11111, 0b10011, 0b10111, 0b10101, 0b11111]
    stop = [0b11111, 0b11111, 0b11111, 0b11111, 0b11111]
    circle = [0b01110, 0b10001, 0b10001, 0b10001, 0b01110]
    play = [0b10000, 0b11100, 0b11111, 0b11100, 0b10000]


Pixel = Tuple[int, int, int]
Color = Tuple[int, int, int]
Point = Tuple[int, int]
ImageData = List[List[Pixel]]

png_image_cached_gb = None
png_image_cached_width = None
png_image_cached_height = None


def interpolate_color(color1 , color2 , factor )  :
    """Interpolate between two colors by a given factor (0.0 to 1.0)."""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return (r, g, b)


class ColorSpectrum:
    # Class variables for each color
    Black  = (0, 0, 0)
    White  = (255, 255, 255)
    Red  = (255, 0, 0)
    Green  = (0, 255, 0)
    Blue  = (0, 0, 255)
    Yellow  = (255, 255, 0)
    Cyan  = (0, 255, 255)
    Magenta  = (255, 0, 255)
    Silver  = (192, 192, 192)
    Gray  = (128, 128, 128)
    Maroon  = (128, 0, 0)
    Olive  = (128, 128, 0)
    Purple  = (128, 0, 128)
    Teal  = (0, 128, 128)
    Navy  = (0, 0, 128)

    # Generate colors in the spectrum
    for i in range(256):
        vars()[f"Color_{i}"] = (i, i, i)  # Simple grayscale spectrum for demonstration

    @staticmethod
    def hsv_to_rgb(h , s , v )  :
        """
        Convert a color from HSV (Hue, Saturation, Value) color space to RGB (Red, Green, Blue) color space.

        :param h: The hue value, ranging from 0.0 to 1.0.
        :type h 
        :param s: The saturation value, ranging from 0.0 to 1.0.
        :type s 
        :param v: The value (brightness) value, ranging from 0.0 to 1.0.
        :type v 
        :return: A tuple representing the RGB color values, each ranging from 0 to 255.
        :rtype 
        """
        if s == 0.0:
            v = int(v * 255)
            return (v, v, v)

        i = int(h * 6.0)  # Assume h is [0, 1]
        f = (h * 6.0) - i
        p = int(255 * v * (1.0 - s))
        q = int(255 * v * (1.0 - s * f))
        t = int(255 * v * (1.0 - s * (1.0 - f)))
        v = int(v * 255)
        i = i % 6

        if i == 0:
            return (v, t, p)
        if i == 1:
            return (q, v, p)
        if i == 2:
            return (p, v, t)
        if i == 3:
            return (p, q, v)
        if i == 4:
            return (t, p, v)
        if i == 5:
            return (v, p, q)

    @staticmethod
    def rgb_to_hsv(r , g , b )  :
        """
        Convert RGB color values to HSV color space.

        :param r: The red component of the RGB color (0-255).
        :type r 
        :param g: The green component of the RGB color (0-255).
        :type g 
        :param b: The blue component of the RGB color (0-255).
        :type b 

        :return: The corresponding HSV color values (h, s, v).
        :rtype: Tuple[float, float, float]

        :raises: None

        The function takes the red, green, and blue components of an RGB color and converts them to the corresponding
        hue, saturation, and value components in the HSV color space. The RGB values should be in the range of 0 to 255.

        The function returns a tuple containing the hue, saturation, and value components of the HSV color, where:
        - h (float): The hue component of the HSV color (0-1).
        - s (float): The saturation component of the HSV color (0-1).
        - v (float): The value component of the HSV color (0-1).
        """
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        maxc = max(r, g, b)
        minc = min(r, g, b)
        v = maxc
        if minc == maxc:
            return 0.0, 0.0, v
        s = (maxc - minc) / maxc
        rc = (maxc - r) / (maxc - minc)
        gc = (maxc - g) / (maxc - minc)
        bc = (maxc - b) / (maxc - minc)
        if r == maxc:
            h = bc - gc
        elif g == maxc:
            h = 2.0 + rc - bc
        else:
            h = 4.0 + gc - rc
        h = (h / 6.0) % 1.0
        return h, s, v

    @classmethod
    def adjust_color(cls, color , h , s , v )  :
        # Convert the color to HSV
        current_h, current_s, current_v = cls.rgb_to_hsv(*color)

        # Adjust HSV values
        new_h = (current_h + h) % 1.0
        new_s = min(max(0.0, current_s * s), 1.0)
        new_v = min(max(0.0, current_v * v), 1.0)

        # Convert back to RGB
        return cls.hsv_to_rgb(new_h, new_s, new_v)

    @classmethod
    def adjust_brightness(cls, color , brightness_factor )  :
        # Convert the color to HSV
        h, s, v = cls.rgb_to_hsv(*color)

        # Adjust the brightness
        v = min(max(0.0, v * brightness_factor), 1.0)

        # Convert back to RGB
        return cls.hsv_to_rgb(h, s, v)

class ImageSection:
    def __init__(self,x, y, width, height):
        self.x = x
        self.y = y
        self.width  = width
        self.height  = height
        self.data = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

    def draw_pixel(self, x, y, color):
        """
        Draws a pixel at the specified coordinates with the given color. Will not draw outside the image boundaries.

        :param x: The x-coordinate of the pixel.
        :type x
        :param y: The y-coordinate of the pixel.
        :type y
        :param color: The color of the pixel.
        :type color 
        :return: None
        :rtype: None
        """
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.data[y][x] = color


class PngImage:
    def __init__(
        self, width , height , bit_depth  = 8, color_type  = 2
    )  :
        self.width  = width
        self.height  = height
        self.bit_depth  = bit_depth
        self.color_type  = color_type
        self.clear()
        self.HEADER = b"\x89PNG\r\n\x1A\n"

    def __get_checksum(self, chunk_type: bytes, data: bytes)  :
        checksum = zlib.crc32(chunk_type)
        checksum = zlib.crc32(data, checksum)
        return checksum

    def __chunk(self, out: BinaryIO, chunk_type: bytes, data: bytes)  :
        out.write(struct.pack(">I", len(data)))
        out.write(chunk_type)
        out.write(data)

        checksum = self.__get_checksum(chunk_type, data)
        out.write(struct.pack(">I", checksum))

    def __make_ihdr(self)  :
        return struct.pack(
            ">2I5B", self.width, self.height, self.bit_depth, self.color_type, 0, 0, 0
        )

    def __encode_data(self):
        ret = []
        for row in self.data:
            ret.append(0)

            color_values = [color_value for pixel in row for color_value in pixel]
            ret.extend(color_values)
        return ret

    def __compress_data(self, data)  :
        data_bytes = bytearray(data)
        return zlib.compress(data_bytes)

    def __make_idat(self)  :
        encoded_data = self.__encode_data()
        compressed_data = self.__compress_data(encoded_data)
        return compressed_data

    def __dump_png(self, out: BinaryIO)  :
        out.write(self.HEADER)  # start by writing the header
        assert len(self.data) > 0  # assume we were not given empty image data
        ihdr_data = self.__make_ihdr()
        self.__chunk(out, b"IHDR", ihdr_data)
        compressed_data = self.__make_idat()
        self.__chunk(out, b"IDAT", data=compressed_data)
        self.__chunk(out, b"IEND", data=b"")

    def clear(self):
            self.data: ImageData = [
                [(0, 0, 0) for _ in range(self.width)] for _ in range(self.height)
            ]

    def draw_pixel(self, x , y , color ):
        """
        Draws a pixel at the specified coordinates with the given color. Will not draw outside the image boundaries.

        :param x: The x-coordinate of the pixel.
        :type x 
        :param y: The y-coordinate of the pixel.
        :type y 
        :param color: The color of the pixel.
        :type color 
        :return: None
        :rtype: None
        """
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.data[y][x] = color

    def draw_pixel_raw(self, x , y , color ):
        """
        Draws a pixel at the specified coordinates with the given color

        :param x: The x-coordinate of the pixel.
        :type x 
        :param y: The y-coordinate of the pixel.
        :type y 
        :param color: The color of the pixel.
        :type color 
        :return: None
        :rtype: None
        """
        self.data[y][x] = color

    def save_png(self, filename )  :
        """
        Saves the image as a PNG file.

        :param filename: The name of the file to save the image to.
        :type filename 

        :return: None
        :rtype: None
        """
        with open(filename, "wb") as out:
            self.__dump_png(out)

    def sub_image(self, iMin , iMax ):
        """
        Returns a sub-image of the current image, defined by the minimum and maximum points.

        :param min: The minimum point of the sub-image.
        :type min 
        :param max: The maximum point of the sub-image.
        :type max 
        :return: A new PngImage object representing the sub-image.
        :rtype 
        """
        x1, y1 = iMin
        x2, y2 = iMax

        # Ensure coordinates are within image bounds and properly ordered
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        x1 = max(0, min(x1, len(self.data[0]) - 1))
        x2 = max(0, min(x2, len(self.data[0]) - 1))
        y1 = max(0, min(y1, len(self.data) - 1))
        y2 = max(0, min(y2, len(self.data) - 1))

        # Extract the sub-image
        sub_image = PngImage(x2 - x1, y2 - y1)
        for y in range(y1, y2):
            for x in range(x1, x2):
                sub_image.draw_pixel(x - x1, y - y1, self.data[y][x])
        return sub_image

    def to_png_buffer(self):
        """
        Converts the image to a PNG format and returns it as a BytesIO object.

        :return: A BytesIO object containing the PNG image data.
        :rtype: BytesIO
        """
        out = BytesIO()
        self.__dump_png(out)
        out.seek(0)
        return out


def scale_bitmap_font(font, char_width, char_height, scale_factor):
    scaled_font = {}
    for char, bitmap in font.items():
        scaled_bitmap = []
        for row in bitmap:
            expanded_row = []
            for bit in range(char_width):
                if row & (1 << (char_width - bit - 1)):
                    expanded_row.extend([1] * scale_factor)
                else:
                    expanded_row.extend([0] * scale_factor)
            for _ in range(scale_factor):
                scaled_row = 0
                for bit in expanded_row:
                    scaled_row = (scaled_row << 1) | bit
                scaled_bitmap.append(scaled_row)
        scaled_font[char] = scaled_bitmap
    return scaled_font


class PngDrawing:

    @staticmethod
    def draw_line(
        img , point1, point2, color, thickness  = 1
    )  :
        """
        Draws a line on the given image between two points with the specified color and thickness.

        :param img: The image on which to draw the line.
        :type img 
        :param point1: The starting point of the line.
        :type point1 
        :param point2: The ending point of the line.
        :type point2 
        :param color: The color of the line.
        :type color 
        :param thickness: The thickness of the line. Defaults to 1.
        :type thickness 
        """

        def draw_pixel(x , y , img , color )  :
            image_data = img.data
            if 0 <= x < len(image_data[0]) and 0 <= y < len(image_data):
                img.draw_pixel(x, y, color)

        def draw_thick_pixel(
            x , y , img , color , thickness 
        )  :
            for dx in range(-thickness // 2 + 1, thickness // 2 + 1):
                for dy in range(-thickness // 2 + 1, thickness // 2 + 1):
                    draw_pixel(x + dx, y + dy, img, color)

        x1, y1 = point1
        x2, y2 = point2

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            draw_thick_pixel(x1, y1, img, color, thickness)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
    @staticmethod
    def draw_icon(img, icon: list, x: int, y: int, color: tuple, background_color = (0, 0, 0)):
        """
        Draw an icon on the given image at the specified coordinates.

        :param img: The image on which to draw the icon.
        :type img 
        :param x: The x-coordinate of the top-left corner of the icon.
        :type x 
        :param y: The y-coordinate of the top-left corner of the icon.
        :type y 
        :param icon: The icon to draw.
        :type icon 
        :return: None
        :rtype: None
        """

        def get_icon_width(icon):
            width = 0
            for line in icon:
                width = max(width, len(bin(line)) - 2)

            return width

        icon_width = get_icon_width(icon)

        for i, line in enumerate(icon):
            for bit_position in range(icon_width):
                bit = line >> (icon_width - bit_position - 1)
                if bool(bit & 1):
                    img.draw_pixel(x + bit_position, y + i, color)
                else:
                    img.draw_pixel(x + bit_position, y + i, background_color)

    @staticmethod
    def draw_rectangle(
        img , x , y , width , height , color 
    )  :
        """
        Draw a rectangle on the given image.

        :param img: The image on which to draw the rectangle.
        :type img 
        :param x: The x-coordinate of the top-left corner of the rectangle.
        :type x 
        :param y: The y-coordinate of the top-left corner of the rectangle.
        :type y 
        :param width: The width of the rectangle.
        :type width 
        :param height: The height of the rectangle.
        :type height 
        :param color: The color of the rectangle.
        :type color 
        :return: None
        :rtype: None
        """
        for i in range(height):
            for j in range(width):
                img.draw_pixel(x + j, y + i, color)

    @staticmethod
    def draw_rectangle_outline(
        image ,
        min_point ,
        max_point ,
        color ,
        thickness = 1 ,
    )  :
        """
        Draws the outline of a rectangle on the given image.

        :param image: The image on which to draw the rectangle outline.
        :type image 
        :param min_point: The minimum point of the rectangle (top-left corner).
        :type min_point 
        :param max_point: The maximum point of the rectangle (bottom-right corner).
        :type max_point 
        :param color: The color of the rectangle outline.
        :type color 
        :param thickness: The thickness of the rectangle outline.
        :type thickness 
        :return: None
        :rtype: None
        """
        x_min, y_min = min_point
        x_max, y_max = max_point

        # Draw the four sides of the rectangle
        PngDrawing.draw_line(
            image, (x_min, y_min), (x_max, y_min), color, thickness
        )  # Top side
        PngDrawing.draw_line(
            image, (x_min, y_max), (x_max, y_max), color, thickness
        )  # Bottom side
        PngDrawing.draw_line(
            image, (x_min, y_min), (x_min, y_max), color, thickness
        )  # Left side
        PngDrawing.draw_line(
            image, (x_max, y_min), (x_max, y_max), color, thickness
        )  # Right side

    @staticmethod
    def draw_circle(
        img , x , y , radius , color 
    )  :
        """
        Draw a circle on the given image.

        :param img: The image on which to draw the circle.
        :type img 
        :param x: The x-coordinate of the center of the circle.
        :type x 
        :param y: The y-coordinate of the center of the circle.
        :type y 
        :param radius: The radius of the circle.
        :type radius 
        :param color: The color of the circle.
        :type color 
        :return: None
        :rtype: None
        """
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i ** 2 + j ** 2 <= radius ** 2:
                    img.draw_pixel(x + i, y + j, color)

    @staticmethod
    def draw_circle_outline(
        img , x , y , radius , color , thickness  = 1
    )  :
        """
        Draw the outline of a circle on the given image.

        :param img: The image on which to draw the circle outline.
        :type img 
        :param x: The x-coordinate of the center of the circle.
        :type x 
        :param y: The y-coordinate of the center of the circle.
        :type y 
        :param radius: The radius of the circle.
        :type radius 
        :param color: The color of the circle outline.
        :type color 
        :param thickness: The thickness of the circle outline.
        :type thickness 
        :return: None
        :rtype: None
        """
        x0, y0, radius = x, y, radius
        f = 1 - radius
        ddf_x = 1
        ddf_y = -2 * radius
        x = 0
        y = radius

        img.draw_pixel(x0, y0 + radius, color)
        img.draw_pixel(x0, y0 - radius, color)
        img.draw_pixel(x0 + radius, y0, color)
        img.draw_pixel(x0 - radius, y0, color)

        while x < y:
            if f >= 0:
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x

            img.draw_pixel(x0 + x, y0 + y, color)
            img.draw_pixel(x0 - x, y0 + y, color)
            img.draw_pixel(x0 + x, y0 - y, color)
            img.draw_pixel(x0 - x, y0 - y, color)
            img.draw_pixel(x0 + y, y0 + x, color)
            img.draw_pixel(x0 - y, y0 + x, color)
            img.draw_pixel(x0 + y, y0 - x, color)
            img.draw_pixel(x0 - y, y0 - x, color)   

    @staticmethod
    def generate_gradient_rectangle(
        img ,
        start_point ,
        end_point ,
        start_color ,
        end_color ,
    )  :
        """Generate a rectangle with a gradient from start_color to end_color."""
        x1, y1 = start_point
        x2, y2 = end_point
        img_data = img.data
        # Ensure coordinates are within image bounds and properly ordered
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        width = x2 - x1 + 1
        height = y2 - y1 + 1

        for y in range(height):
            factor_y = y / (height - 1)  # Interpolation factor based on row
            for x in range(width):
                factor_x = x / (width - 1)  # Interpolation factor based on column
                factor = (factor_y + factor_x) / 2
                color = interpolate_color(start_color, end_color, factor)
                img.draw_pixel(x1 + x, y1 + y, color)

    @staticmethod
    def draw_text(
        img ,
        text ,
        x ,
        y ,
        scale  = 1,
        spacing  = 1,
        color  = (255, 255, 255),
    )  :
        """
        Draws text on the given image at the specified coordinates.

        :param img: The image on which to draw the text.
        :type img 
        :param text: The text to be drawn.
        :type text 
        :param x: The x-coordinate of the starting position of the text.
        :type x 
        :param y: The y-coordinate of the starting position of the text.
        :type y 
        :param scale: The scale factor for the text size. Defaults to 1.
        :type scale , optional
        :param spacing: The spacing between characters. Defaults to 1.
        :type spacing , optional
        :param color: The color of the text. Defaults to (255, 255, 255).
        :type color , optional
        :return: None
        :rtype: None
        """
        char_width = 5
        char_height = 7
        spacing = spacing

        if scale > 1:
            font_5x7_scaled = scale_bitmap_font(
                font_5x7, char_width, char_height, scale
            )
            char_width *= scale
            char_height *= scale
        else:
            font_5x7_scaled = font_5x7
        text = str(text)
        for i, char in enumerate(text):
            if char in font_5x7_scaled:
                character = font_5x7_scaled[char]
                start_x = x + i * (char_width + spacing)
                for j, line in enumerate(character):
                    start_y = y + j
                    for bit_position in range(char_width):
                        bit = (line >> (char_width - bit_position - 1)) & 1
                        if bool(bit):
                            img.draw_pixel(start_x + bit_position, start_y, color)

    @staticmethod
    def draw_fader(image , value , x , y , width  = 9, height  = 45, color  = (255,255,255)):
        value = max(0, min(1, float(value)))
        fader_height = int(height * value)
        end_x = x + width
        start_y = y + height - fader_height
        end_y = y + height

        # Horizontal Line
        PngDrawing.draw_line(
            image, (x, start_y), (x + width, start_y), color
        )
        PngDrawing.draw_line(image, (end_x, start_y), (end_x, end_y), color)

    @staticmethod
    def draw_horizontal_meter(
        image ,
        value ,
        x ,
        y ,
        width  = 45,
        height  = 9,
        color  = (255, 255, 255),
    )  :
        value = max(0, min(1, float(value)))
        meter_width = int(width * value)

        PngDrawing.draw_rectangle_outline(
            image, (x, y), (x + width, y + height), color, 1
        )
        PngDrawing.draw_rectangle(image, x, y, meter_width, height, color)

    @staticmethod
    def draw_toggle_button(
        image ,
        label ,
        value: bool,
        x ,
        y ,
        width  = 0,
        height  = 0,
        color  = (255, 255, 255),
        scale  = 1,
        padding_x  = 2,
        padding_y  = 2,
    )  :

        text_width = len(str(label)) * (scale * 6)
        text_height = scale * 7
        width = text_width + (padding_x * 2) if width == 0 else width
        height = text_height + (padding_y * 2) if height == 0 else height
        start_x = x + (width - text_width) // 2
        start_y = y + (height - text_height) // 2
        text_color  = (255, 255, 255)
        if value:
            PngDrawing.draw_rectangle(image, x, y, width, height, color)
            text_color = (0, 0, 0)
        PngDrawing.draw_rectangle_outline(
            image, (x, y), (x + width, y + height), color, 1
        )
        PngDrawing.draw_text(
            image, label, start_x, start_y, scale=1, color=text_color
        )
    @staticmethod
    def draw_pan(
        image ,
        pan ,
        x ,
        y ,
        width  = 27,
        height  = 10,
        color  = (255, 255, 255),
    ):
        # Pan is int from -1 to 1
        pan = max(-1, min(1, float(pan)))
        pan_width = int(width / 2 * pan)
        pan_start_x = (width // 2)
        if pan < 0:
            pan_start_x += pan_width
        PngDrawing.draw_rectangle_outline(
            image, (x, y), (x + width, y + height), color, 1
        )
        PngDrawing.draw_rectangle(
            image, pan_start_x, y, abs(pan_width), height, color
        )
        if pan == float(0):
            PngDrawing.draw_line(
                image,
                (x + width // 2, y),
                (x + width // 2, y + height),
                (255, 255, 255),
            )

    @staticmethod
    def draw_vertical_meter(
        image ,
        value ,
        x ,
        y ,
        width  = 14,
        height  = 45,
        color  = (255, 255, 255),
    ):
        value = max(0, min(1, float(value)))
        meter_height = int(height * value)
        start_y = y + height - meter_height

        PngDrawing.draw_rectangle_outline(
            image, (x, y), (x + width, y + height), color, 1
        )
        PngDrawing.draw_rectangle(image, x, start_y, width, meter_height, color)

    @staticmethod
    def draw_knob(
        image ,
        value ,
        x ,
        y ,
        size  = 20,
        color  = (255, 255, 255),
        range  = 280,
        filled: bool = False
    ):
        radius = size // 2
        value = max(0, min(1, float(value)))

        # Draw the dial on the circle outline using the value ina circular fashion. Maybe use pi, sin, cos
        range = max(180, min(360, range))
        angle = (range - (value * range)) - ((360 - range) // 2)
        offset = 4

        # Get point ratios from angle
        y_ratio = sin(rad(angle))
        x_ratio = cos(rad(angle))

        # Get start and end points
        x_start = int((0 + offset) * x_ratio)
        y_start = int((0 + offset) * y_ratio)
        y_end = int(radius * y_ratio)
        x_end = int(radius  * x_ratio)

        # Invert y values
        y_start = abs(y_start) if y_start < 0 else -abs(y_start)
        y_end = abs(y_end) if y_end < 0 else -abs(y_end)

        # Shift into position
        x_start += x + radius
        y_start += y + radius
        x_end += x + radius
        y_end += y + radius
        if filled == False:
            PngDrawing.draw_circle_outline(image, x + radius, y + radius, radius, color, 1)
            PngDrawing.draw_line(image, (x_start, y_start), (x_end, y_end), color, 1)
        else:
            PngDrawing.draw_circle(image, x + radius, y + radius, radius, color)
            PngDrawing.draw_line(image, (x + radius, y + radius), (x_end, y_end), (0,0,0), 1)

from typing import NamedTuple, Tuple

aquamarine = (127,255,212)
azure = (240,255,255)
beige = (245,245,220)
bisque = (255,228,196)
brown = (165,42,42)
chocolate = (210,105,30)
coral = (255,127,80)
crimson = (220,20,60)
gold = (255,215,0)
gray = (128,128,128)
honeydew = (240,255,240)
indigo = (75,0,130)
ivory = (255,255,240)
khaki = (240,230,140)
lavender = (230,230,250)
lime = (0,255,0)
maroon = (128,0,0)
navy = (0,0,128)
olive = (128,128,0)
plum = (221,160,221)
salmon = (250,128,114)
silver = (192,192,192)
teal = (0, 128, 128)
thistle = (216,191,216)
turquoise = (64,224,208)
violet = (238,130,238)


class ColorTriplet(NamedTuple):
    """The red, green, and blue components of a color."""

    red: int
    """Red component in 0 to 255 range."""
    green: int
    """Green component in 0 to 255 range."""
    blue: int
    """Blue component in 0 to 255 range."""

    @property
    def hex(self) -> str:
        """get the color triplet in CSS style."""
        red, green, blue = self
        return f"#{red:02x}{green:02x}{blue:02x}"

    @property
    def rgb(self) -> str:
        """The color in RGB format.

        Returns:
            str: An rgb color, e.g. ``"rgb(100,23,255)"``.
        """
        red, green, blue = self
        return f"rgb({red},{green},{blue})"

    @property
    def normalized(self) -> Tuple[float, float, float]:
        """Convert components into floats between 0 and 1.

        Returns:
            Tuple[float, float, float]: A tuple of three normalized colour components.
        """
        red, green, blue = self
        return red / 255.0, green / 255.0, blue / 255.0

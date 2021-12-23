import os
from enum import Enum
from typing import Optional

__all__ = [
    "ColorDepth",
]


class ColorDepth(str, Enum):
    """
    The bit depth specifies the number of bits used for each color component
    """

    value: str

    #: 2 colors, often black and white
    one_bit = "one_bit"

    #: ANSI Colors. 16 colors
    four_bit = "four_bit"

    #: The default. 256 colors
    eight_bit= "eight_bit"

    #: 24 bit True color.
    twenty_four_bit = "twenty_four_bit"

    # Aliases.
    MONOCHROME = one_bit
    ANSI_COLORS_ONLY = four_bit
    DEFAULT = eight_bit
    TRUE_COLOR = twenty_four_bit

    @classmethod
    def from_env(cls) -> Optional["ColorDepth"]:
        """
        Return the color depth if the $QUO_COLOR_DEPTH environment
        variable has been set.

        This is a way to enforce a certain color depth in all quo
        applications.
        """
        # Check the `QUO_COLOR_DEPTH` environment variable.
        all_values = [i.value for i in ColorDepth]
        if os.environ.get("QUO_COLOR_DEPTH") in all_values:
            return cls(os.environ["QUO_COLOR_DEPTH"])

        return None

    @classmethod
    def default(cls) -> "ColorDepth":
        """
        Return the default color depth for the default output.
        """
        from .defaults import create_output

        return create_output().get_default_color_depth()

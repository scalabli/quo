from .exceptions import (
        Abort,
        UsageError,
        BadParameter,
        MissingParameter,
        NoSuchApp,
        Outlier,
        BadAppUsage,
        BadArgUsage,
        FileError,
        Exit,
        ValidationError
        )

# lass ConsoleError(Exception):
 #   """An error in console operation."""


#lass StyleError(Exception):
#    """An error in styles."""


#ass StyleSyntaxError(ConsoleError):
 #   """Style was badly formatted."""


#ss MissingStyle(StyleError):
   # """No such style."""


#ss StyleStackError(ConsoleError):
  #  """Style stack is invalid."""


from .exceptions import (
        ConsoleError,
        NotRenderableError,
        MarkupError,
        )
  #  """Markup was badly formatted."""


#ss LiveError(ConsoleError):
  #  """Error related to Live display."""


#ss NoAltScreen(ConsoleError):
  #  """Alt screen mode was required."""

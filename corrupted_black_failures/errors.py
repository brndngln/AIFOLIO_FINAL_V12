"""SAFE AI MODULE"""

"SAFE AI MODULE"
"SAFE AI MODULE"


class ConsoleError(Exception):
    pass


class StyleError(Exception):
    pass


class StyleSyntaxError(ConsoleError):
    pass


class MissingStyle(StyleError):
    pass


class StyleStackError(ConsoleError):
    pass


class NotRenderableError(ConsoleError):
    pass


class MarkupError(ConsoleError):
    pass


class LiveError(ConsoleError):
    pass


class NoAltScreen(ConsoleError):
    pass

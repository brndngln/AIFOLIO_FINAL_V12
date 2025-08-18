"""Clean replacement for corrupted PngImagePlugin.py module."""

from typing import Any, Optional


class PngImageFile:
    """PNG image file handler placeholder."""

    def __init__(self, fp: Any) -> None:
        self.fp = fp
        self.format = "PNG"
        self.mode = "RGB"
        self.size = (0, 0)

    def load(self) -> None:
        """Load image data."""
        pass

    def save(self, fp: Any, **kwargs: Any) -> None:
        """Save image data."""
        pass


class PngInfo:
    """PNG metadata info placeholder."""

    def __init__(self) -> None:
        self.chunks: list[tuple] = []

    def add_text(self, key: str, value: str) -> None:
        """Add text chunk."""
        self.chunks.append(("tEXt", key, value))


def _accept(prefix: bytes) -> bool:
    """Check if file is PNG format."""
    return prefix.startswith(b"\x89PNG\r\n\x1a\n")


def _save(im: Any, fp: Any, filename: str, **kwargs: Any) -> None:
    """Save PNG image."""
    pass


try:
    from PIL import Image

    Image.register_open(PngImageFile.format, PngImageFile, _accept)
    Image.register_save(PngImageFile.format, _save)
    Image.register_extension(PngImageFile.format, ".png")
    Image.register_mime(PngImageFile.format, "image/png")
except ImportError:
    pass

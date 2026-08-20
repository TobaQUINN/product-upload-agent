from dataclasses import dataclass


@dataclass
class ImageInput:
    """
    Represents an image that the Product Upload Agent should process.
    """

    source: str
    identifier: str

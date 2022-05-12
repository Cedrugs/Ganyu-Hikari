from dataclasses import dataclass

__all__ = ('Colour', )


@dataclass(frozen=True)
class Colour:
    blue: int = '#99ebec'

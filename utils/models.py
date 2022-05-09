from dataclasses import dataclass


__all__ = ('Colour', )


@dataclass(frozen=True)
class Colour:
    Blue: int = '#99ebec'

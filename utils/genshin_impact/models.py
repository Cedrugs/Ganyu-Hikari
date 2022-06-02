from dataclasses import dataclass


__all__ = ('GenshinWeapon', )


@dataclass(frozen=True)
class GenshinWeapon:
    _id: str
    name: str
    description: str
    icon: str
    type: str
    rarity: int
    max_level: int
    base_atk: int
    substat: str
    sub_value: float
    passive: dict
    ascension: dict
    stats: dict
    location: str

from dataclasses import dataclass


__all__ = ('GenshinWeapon', 'GenshinStatistics', 'GenshinAscensionMaterial', 'GenshinWeaponPassive')


@dataclass(frozen=True)
class GenshinStatistics:
    list: list
    visual: str


@dataclass(frozen=True)
class GenshinAscensionMaterial:
    levels: dict
    summary: dict


@dataclass(frozen=True)
class GenshinWeaponPassive:
    name: str
    description: str


@dataclass(frozen=True)
class GenshinWeapon:
    id: str
    name: str
    description: str
    icon: str
    type: str
    rarity: int
    max_level: int
    base_atk: int
    substat: str
    sub_value: float
    passive: GenshinWeaponPassive
    ascension: GenshinAscensionMaterial
    stats: GenshinStatistics
    location: str

import datetime
from dataclasses import dataclass


__all__ = (
    'GenshinWeapon', 'GenshinStatistics', 'GenshinAscensionMaterial', 'GenshinWeaponPassive', 'WeaponButtonType',
    'DailyRewardInfo'
)


@dataclass(frozen=True)
class WeaponButtonType:
    details: int = 'details'
    ascension: int = 'ascension'
    statistic: int = 'statistic'


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


@dataclass(frozen=True)
class DailyRewardInfo:
    claimed_rewards: int
    missed_rewards: int
    last_claimed_rewards: dict
    claim_time: datetime.datetime

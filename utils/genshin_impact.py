import genshin
import difflib


__all__ = ('get_wish', 'get_weapon_info', 'get_character_info')


banner_dict = {
    'Permanent Wish': 200,
    'Character Event Wish': 301,
    'Weapon Event Wish': 302
}


async def get_wish(authkey, banner_type: list):
    client = genshin.GenshinClient(authkey=authkey)
    wish_history = {f'{x}': [] for x in banner_type}
    wish_uid = None

    async for wish in client.wish_history(banner_type=banner_type):
        if wish_uid is None:
            wish_uid = wish.uid
        wish_history[str(banner_dict[wish.banner_name])].append(
            {
                'Type': wish.type,
                'Name': shorten_name(wish.name),
                'Time': wish.time.strftime('%x %X'),
                'Rarity': wish.rarity,
                'Pity': None,
                'Banner Type': wish.banner_type
            }
        )
    wish_history.update(
        {
            "UID": wish_uid,
        }
    )
    for data in banner_type:
        wish_history[str(data)].reverse()
    await client.close()
    wish_history = sort_wish(wish_history, banner_type)
    for data in banner_type:
        wish_history[str(data)].reverse()
    return wish_history


def sort_wish(wish: dict, banner_type: list) -> dict:
    for banner in banner_type:
        pity = 1
        for data in wish[str(banner)]:
            if data['Rarity'] == 5:
                data['Pity'] = pity
                pity = 1
            else:
                data['Pity'] = pity
                pity += 1
    return wish


def shorten_name(name: str) -> str:
    if not len(name) > 14:
        return name
    divided_name = name.split()
    mid_value = round(len(divided_name) / 2)
    new_name = f'{" ".join(divided_name[0:mid_value])}\n{" ".join(divided_name[mid_value:len(divided_name)])}'
    return new_name


async def get_weapon_info(key: str, collection, weapon_key):
    weapon_name = difflib.get_close_matches(key, weapon_key, cutoff=0.3)
    if not weapon_name:
        return None
    return await collection.find_by_id(weapon_name[0])


async def get_character_info(key: str, collection, character_key):
    character_name = difflib.get_close_matches(key, character_key, cutoff=0.3)
    if not character_name:
        return None
    return await collection.find_by_id(character_name[0])

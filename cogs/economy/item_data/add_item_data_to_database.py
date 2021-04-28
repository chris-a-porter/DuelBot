from rs_api.get_item_value import get_item_value
import globals
import psycopg2
import json
from psycopg2.extensions import register_adapter
from psycopg2 import extras
import os
from helpers.math_helpers import numify
from functools import reduce

DATABASE_URL = os.environ['DATABASE_URL']


def get_osrsbox_data(item_id):
    for item in globals.all_db_items:
        if item.id == item_id:
            return item


# Recursive call through an attribute chain to get the ultimate value.
def deepgetattr(obj, attr):

    try:
        return reduce(getattr, attr.split('.'), obj)
    except Exception as e:
        return 0


def stringify_json(requirement_json):

    print("THE JSON", requirement_json)
    if json is None or type(json) is not dict:
        return json.dumps({})
    else:
        return json.dumps(requirement_json)


async def add_item_data_to_database(item_id):
    item_info = get_osrsbox_data(item_id)
    item_price = await get_item_value(item_id)

    sql = f"""
        INSERT INTO item_references
        (
        id,
        name,
        tradeable,
        placeholder,
        equipable,
        price,
        low_alch_value,
        high_alch_value,
        weight,
        examine,
        attack_stab,
        attack_slash,
        attack_crush,
        attack_magic,
        attack_ranged,
        defence_stab,
        defence_slash,
        defence_crush,
        defence_magic,
        defence_ranged,
        melee_strength,
        ranged_strength,
        magic_damage,
        prayer,
        slot,
        attack_speed,
        weapon_type
        )
        VALUES
        (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )
        ON CONFLICT DO NOTHING
        """
    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql, (
            item_id,
            item_info.name.replace("'", "\'"),
            item_info.tradeable,
            item_info.placeholder,
            item_info.equipable,
            numify(item_price),
            item_info.lowalch,
            item_info.highalch,
            item_info.weight,
            item_info.examine.replace("'", "\'"),
            deepgetattr(item_info, 'equipment.attack_stab'),
            deepgetattr(item_info, 'equipment.attack_slash'),
            deepgetattr(item_info, 'equipment.attack_crush'),
            deepgetattr(item_info, 'equipment.attack_magic'),
            deepgetattr(item_info, 'equipment.attack_ranged'),
            deepgetattr(item_info, 'equipment.defence stab'),
            deepgetattr(item_info, 'equipment.defence_slash'),
            deepgetattr(item_info, 'equipment.defence_crush'),
            deepgetattr(item_info, 'equipment.defence_magic'),
            deepgetattr(item_info, 'equipment.defence_ranged'),
            deepgetattr(item_info, 'equipment.melee_strength'),
            deepgetattr(item_info, 'equipment.ranged_strength'),
            deepgetattr(item_info, 'equipment.magic_damage'),
            deepgetattr(item_info, 'equipment.equipment.prayer'),
            deepgetattr(item_info, 'equipment.slot'),
            deepgetattr(item_info, 'weapon.attack_speed'),
            deepgetattr(item_info, 'weapon.weapon_type')
        ))
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error adding item to database with ID: {item_id}.", error)
        return False
    finally:
        if conn is not None:
            conn.close()
    return True

from PIL import Image, ImageDraw, ImageFont
import psycopg2
import os
import math
import io
import discord
from helpers.math_helpers import short_numify
from ..loot.generate_loot_image import scale_image, scale_image_to_dimension

font = ImageFont.truetype('assets/osrs-font-compact.otf', 160)
bold_font = ImageFont.truetype('assets/osrs-font-bold.ttf', 160)
value_font = ImageFont.truetype('assets/osrs-font-compact.otf', 140)


DATABASE_URL = os.environ['DATABASE_URL']



def add_header_to_bank_image(image, username, value):

    bg = ImageDraw.Draw(image)

    msg = f"{username}'s DuelBot bank - {short_numify(value, 1)} GP"
    # bg.text((0, 0), msg, (255, 152, 31), font=bold_font)

    w, h = bg.textsize(msg, font=bold_font)
    bg.text((((image.size[0] - w) / 2) + 10, 120), msg, fill="black", font=bold_font)
    bg.text(((image.size[0] - w) / 2, 110), msg, (255, 152, 31), font=bold_font)
    return image


# Add an item to the bank
def add_item_to_bank_grid(grid_image, item_image, index):

    row = math.floor(index / 8)
    x_coord = (index % 8) * 420 + int((420 - item_image.size[0]) / 2)
    y_coord = row * 320 + int((320 - item_image.size[1]) / 2)

    grid_image.paste(item_image, (x_coord, y_coord), mask=item_image)

    return grid_image


# Fetch all of the user's bank items
async def fetch_bank_items(ctx):
    sql = f"""SELECT
            u.item_id,
            u.quantity,
            r.price * u.quantity
            FROM
            user_items as u
            LEFT JOIN item_references as r
            ON u.item_id = r.id
            WHERE
            u.user_id = %s
            ORDER BY r.price * quantity DESC"""

    # List element containing the user's slayer experience
    rows = None

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(sql, (ctx.author.id,))
        rows = cur.fetchall()
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error fetching bank items for player with ID: {ctx.author.id}", error)
    finally:
        if conn is not None:
            conn.close()

    return rows


# Generate the bank image for the user
async def generate_bank_image(ctx):

    bank_items = await fetch_bank_items(ctx)

    bank_background = Image.open('assets/BankInterface.png').convert("RGBA")

    price = 0

    for item in bank_items:
        price = price + item[2]

    for num, item in enumerate(bank_items[0:48]):

        item_image = scale_image(Image.open(f'assets/items-icons/{item[0]}.png').convert("RGBA"), 10)

        if item[0] == 995:
            item_image = scale_image(Image.open(f'assets/items-icons/1004.png').convert("RGBA"), 10)

        draw = ImageDraw.Draw(item_image)

        adjusted_price = item[1] if item[1] < 100000 else short_numify(item[1], 1)
        adjusted_color = (255, 255, 0) if item[1] < 100000 else (0, 0, 0) if item[1] < 10000000 else (0, 255, 0)

        draw.text((10, 10), f"{adjusted_price}", (0, 0, 0), font=font)
        draw.text((0, 0), f"{adjusted_price}", adjusted_color, font=font)

        # Calculate coordinates
        row = math.floor(num / 8)
        x_coord = (num % 8) * 610 + int((610 - item_image.size[0]) / 2)
        y_coord = row * 480 + int((480 - item_image.size[1]) / 2)

        bank_background.paste(item_image, (30 + x_coord, 360 + y_coord), mask=item_image)

    add_header_to_bank_image(bank_background, ctx.author.name, price)

    with io.BytesIO() as image_binary:
        bank_background.save(image_binary, 'PNG')
        image_binary.seek(0)

        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))


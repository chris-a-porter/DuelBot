from PIL import Image, ImageDraw, ImageFont
import io
import discord
import math
from helpers.math_helpers import numify, short_numify

font = ImageFont.truetype('assets/osrs-font-compact.otf', 120)
bold_font = ImageFont.truetype('assets/osrs-font-bold.ttf', 160)
value_font = ImageFont.truetype('assets/osrs-font-compact.otf', 140)
image_max_dim = 30


# Scale image up along both axes
def scale_image(image, scale=1):
    image_width = image.size[0] * scale
    image_height = image.size[1] * scale

    return image.resize((image_width, image_height))


# Scale image to max dimension
def scale_image_to_dimension(image, max_dimension):
    image_width = image.size[0]
    image_height = image.size[1]
    aspect_ratio = image_width / image_height

    new_width = max_dimension
    new_height = max_dimension

    if aspect_ratio >= 1:
        new_height = max_dimension / aspect_ratio * 0.9375
        new_width = new_width * 0.9375
    elif aspect_ratio < 1:
        new_width = max_dimension / aspect_ratio * 0.9375
        new_height = new_height * 0.9375

    return image.resize((int(new_width), int(new_height)))


def generate_inventory_grid():
    # Technically a 4 x 7 grid of 42 x 32 squares
    return Image.new("RGBA", (1680, 2240), (84, 75, 64))


def add_header_to_loot_image(image, username):

    bg = ImageDraw.Draw(image)

    msg = f"{username}'s loot"
    # bg.text((0, 0), msg, (255, 152, 31), font=bold_font)

    w, h = bg.textsize(msg, font=bold_font)
    bg.text((((image.size[0] - w) / 2) + 10, 120), msg, fill="black", font=bold_font)
    bg.text(((image.size[0] - w) / 2, 110), msg, (255, 152, 31), font=bold_font)
    return image


def add_footer_value_to_image(image, value):

    str_val = value

    if value > 100000:
        str_val = short_numify(value, 1)
    else:
        str_val = numify(value)

    bg = ImageDraw.Draw(image)

    msg = f"Value: {str_val} GP"
    # bg.text((0, 0), msg, (255, 152, 31), font=bold_font)

    w, h = bg.textsize(msg, font=value_font)
    bg.text((((image.size[0] - w) / 2) + 5, (image.size[1]) - 170), msg, fill="black", font=value_font)
    bg.text((((image.size[0] - w) / 2), (image.size[1]) - 175), msg, (255, 152, 31), font=value_font)
    return image


def add_item_to_inventory_grid(grid_image, item_image, index):

    row = math.floor(index / 4)
    x_coord = (index % 4) * 420 + int((420 - item_image.size[0]) / 2)
    y_coord = row * 320 + int((320 - item_image.size[1]) / 2)

    grid_image.paste(item_image, (x_coord, y_coord), mask=item_image)

    return grid_image


# Generate an image of some loot
async def generate_loot_image(ctx, loot):

    looting_bag_background = scale_image(Image.open('assets/LootingBag.png').convert("RGBA"))
    looting_bag_inventory = generate_inventory_grid()

    for num, key in enumerate(loot.keys(), start=0):

        abyssal_whip_image = scale_image(Image.open(f'assets/items-icons/{key}.png').convert("RGBA"), 10)

        abyssal_whip_image = scale_image_to_dimension(abyssal_whip_image, 280)

        draw = ImageDraw.Draw(abyssal_whip_image)

        if loot[key] > 1:
            draw.text((0, 0), f"{loot[key]}", (255, 255, 0), font=font)

        looting_bag_inventory = add_item_to_inventory_grid(looting_bag_inventory, abyssal_whip_image, num)

    looting_bag_background.paste(looting_bag_inventory, (180, 310), mask=looting_bag_inventory)
    add_header_to_loot_image(looting_bag_background, ctx.author.name)
    add_footer_value_to_image(looting_bag_background, 1234567)

    with io.BytesIO() as image_binary:
        looting_bag_background.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import io
import discord
import math

font = ImageFont.truetype('assets/osrs-font-compact.otf', 120)
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

    if aspect_ratio <= 1:
        new_height = max_dimension / aspect_ratio * 0.9375
        new_width = new_width * 0.9375
    elif aspect_ratio > 1:
        new_width = max_dimension / aspect_ratio * 0.9375
        new_height = new_height * 0.9375

    return image.resize((int(new_width), int(new_height)))


def generate_inventory_grid():
    # Technically a 4 x 7 grid of 42 x 32 squares
    return Image.new("RGBA", (1680, 2240), (84, 75, 64))


def add_item_to_inventory_grid(grid_image, item_image, index):

    row = math.floor(index / 4)
    x_coord = (index % 4) * 420 + int((420 - item_image.size[0]) / 2)
    y_coord = row * 320 + int((320 - item_image.size[1]) / 2)

    print(index, x_coord, y_coord)

    grid_image.paste(item_image, (x_coord, y_coord), mask=item_image)

    return grid_image


# Generate an image of some loot
async def generate_loot_image(ctx, loot):

    print('LOOT', loot)

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

    with io.BytesIO() as image_binary:
        looting_bag_background.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

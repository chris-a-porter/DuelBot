from PIL import Image, ImageDraw, ImageFilter, ImageFont
import io
import discord
import math

font = ImageFont.load('assets/osrs-font.ttf')
image_max_dim = 30


# Generate an image of some loot
async def generate_loot_image(ctx, loot):
    looting_bag_background = Image.open('assets/LootingBag.png').convert("RGBA")

    for num, loot_item in enumerate(loot, start=1):

        abyssal_whip_image = Image.open('assets/Abyssal whip.png').convert("RGBA")

        image_width = abyssal_whip_image.size[0]
        image_height = abyssal_whip_image.size[1]
        aspect_ratio = image_width / image_height

        new_width = image_max_dim
        new_height = image_max_dim

        if aspect_ratio <= 1:
            new_height = image_max_dim / aspect_ratio
        elif aspect_ratio > 1:
            new_width = image_max_dim / aspect_ratio

        abyssal_whip_image = abyssal_whip_image.resize((int(new_width), int(new_height)))

        draw = ImageDraw.Draw(abyssal_whip_image)
        draw.text((0, 0), f"123", (0, 0, 0), font=font)

        row = math.ceil(num / 4)
        x_coord = -15 + (num * 41)
        y_coord = -5 + (row * 43)

        looting_bag_background.paste(abyssal_whip_image, (x_coord, y_coord), mask=abyssal_whip_image)

    with io.BytesIO() as image_binary:
        looting_bag_background.save(image_binary, 'PNG')
        image_binary.seek(0)
        await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))

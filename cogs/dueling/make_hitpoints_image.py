from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Creates the hitpoints image
# Parameters:
# Hipoints - int - how many hitpoints are left
# Freeze - bool - is the user frozen
# Poison - bool - is the user poisoned


def make_hitpoints_image(hitpoints, freeze, poison):

    # Red background
    primary = (252, 3, 3)

    #Green hitpoints bar
    secondary = (0, 255, 26)

    if poison == True:
        #Lighter green
        primary = (44, 156, 55)

        #Darker green
        secondary = (112, 219, 123)

    if freeze == True:
        #Lighter blue
        primary = (69, 155, 217)

        #Darker blue
        secondary = (130, 203, 255)

    # Creates the image with width of 40 x 198 (99 x 2), with a background color of the primary var
    img = Image.new('RGB', (198, 40), primary)

    # Adds the remaining HP on top of the background, with 2 * the number of hitpoints remaining as the width
    img.paste(secondary, (0, 0, 2 * hitpoints, 40))

    # Draw the image
    draw = ImageDraw.Draw(img)

    # Load the Runescape font
    font = ImageFont.truetype('assets/osrs-font-bold.ttf', 16)

    # Add text containing info about the remaining HP to the image
    draw.text((80, 10), f"{hitpoints}/99", (0, 0, 0), font=font)

    # Save the image locally
    # Note: this file is created and immediately deleted after the image has been posted to discord
    img.save('./hpbar.png')
from .generate_bank_image import generate_bank_image


async def command_bank(ctx):
    await generate_bank_image(ctx)
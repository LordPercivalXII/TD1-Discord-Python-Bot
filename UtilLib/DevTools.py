import os
from disnake import User, ApplicationCommandInteraction
from disnake.ext.commands import Context
from UtilLib.CommandLevel import CommandHandler


async def lookup_dev_cmd(ctx: Context or ApplicationCommandInteraction, client):
    cmd_handler = CommandHandler(
        min_level=CommandHandler.DEVELOPER,
        user_id=ctx.author.id,
        server=ctx.guild,
        server_data=ctx.server_data_handler
    )

    eligibility = await cmd_handler.check_cmd_req(
        ctx,
        message="This is a restricted command."
    )

    if eligibility is False:
        return

    dev_usr: User = await client.fetch_user(int(os.getenv('DEVELOPER_ID')))
    await ctx.reply(f"USER: {dev_usr.display_name} | {dev_usr.discriminator}")

    for emoji in await ctx.guild.fetch_emojis():
        await ctx.reply(f"EMOJI: {emoji}")
        print(emoji)

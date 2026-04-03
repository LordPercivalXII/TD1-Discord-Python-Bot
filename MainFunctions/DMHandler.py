import datetime
import os
import time
from disnake import Message, DMChannel, User, Embed, CommandInteraction, ApplicationCommandInteraction
from disnake.ext.commands import Context, Cog


class DirectMessageHandler:
    def __init__(self, ctx: Context or ApplicationCommandInteraction, recipient: User):
        self.ctx: Context = ctx
        self.recipient: User = recipient

    async def send_message(self, message):
        embed = Embed(
            title=f"Message to {self.recipient}",
            description=message,
            timestamp=datetime.datetime(
                year=datetime.datetime.now().year,
                month=datetime.datetime.now().month,
                day=datetime.datetime.now().day,
                hour=datetime.datetime.now().hour,
                minute=datetime.datetime.now().minute,
                second=datetime.datetime.now().second
            ),
            colour=0x008369,
        )
        embed.set_footer(text=f"To {self.recipient}")
        embed.set_author(name=self.ctx.author, icon_url=self.ctx.author.avatar.url)
        embed.set_thumbnail(url=self.recipient.avatar.url)

        await self.recipient.send(embed=embed)

    async def send_message_raw(self, message):
        await self.recipient.send(message)


async def dm_cmd(ctx: Context or ApplicationCommandInteraction, recipient: User, message):
    if recipient is None:
        return await ctx.response.send_message(f"Please specify a user to send a DM to.", ephemeral=True) if hasattr(ctx, "response") \
            else await ctx.send(f"Please specify a user to send a DM to.", ephemeral=True)

    if message is None:
        return await ctx.response.send_message(f"Please specify a message.", ephemeral=True) if hasattr(ctx, "response") else \
            await ctx.send(f"Please specify a message.", ephemeral=True)

    dm_method = DirectMessageHandler(ctx, recipient)
    await dm_method.send_message(message)
    await ctx.response.send_message("Message Sent.", ephemeral=True) if hasattr(ctx, "response") else \
        await ctx.send("Message Sent.", ephemeral=True)


async def dm_TD1_cmd(ctx: Context or ApplicationCommandInteraction, client, message):
    if message is None:
        return await ctx.response.send_message(f"Please specify a message.", ephemeral=True) if hasattr(ctx, "response") else \
            await ctx.send(f"Please specify a message.", ephemeral=True)

    dm_method = DirectMessageHandler(
        ctx,
        recipient=await client.fetch_user(int(os.getenv("DEVELOPER_ID")))
    )

    await dm_method.send_message(message)
    await ctx.response.send_message("Message Sent.", ephemeral=True) if hasattr(ctx, "response") else \
        await ctx.send("Message Sent.", ephemeral=True)

import datetime
import os
import subprocess
import sys
import time
from disnake import Activity, ActivityType, Game, Embed, Colour, Intents, ApplicationCommandInteraction, Member, \
    TextChannel, Guild, Emoji, PartialEmoji, Status
from disnake.abc import GuildChannel
from disnake.ext import commands
from disnake.ext.commands import Context
from VersionControl import __version__ as proj_vers, __copyright__ as proj_cpr
from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
from MasterApprenticeLib.TD1_Lib_MasterApprentice_Control import __version__ as log_vers, __copyright__ as log_cpr
from CoFunctions.ServerDataHandler import on_init, get_serverdata_value, update_serverdata_value, allowable_events
from UtilLib.LoggerService import BaseLoggerService
from UtilLib.ServicingPipeline import check_current_version
from UtilLib.EmojiHandler import get_emoji
from UtilLib.CommandLevel import CommandHandler

# ======================================================================================================================
# Core Variables
# Start Time for Bot Uptime based upon comparison
START_TIME = time.time()

# Bot Intents [API]
INTENTS = Intents.all()


# ======================================================================================================================
# Classes
class CoreFunctionService(BaseLoggerService):
    pass


class TD1BotContext(Context):
    pass


class TD1BotClient(commands.Bot):
    """
    Subclass of the discord.py/disnake Bot Class.

    Core Command Handling should go here.
    """
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("~", "?", "!"),
            description="""
            This is a test help command.

            Bot Prefixes: ~ OR ! OR ?
            """,
            owner_id=os.getenv("DEVELOPER_ID"),
            # Removal of test guilds, causing issues to CMD Globalisation
            # test_guilds=[604082560217120778, 569137415051280404, 949322786713788426],
            intents=INTENTS,
            sync_commands_debug=True
        )
        # self.InternalHandler = TD1BotClient()

        # Logger Init - Shift from Raw MasterLogger to Logger Service
        self.master_logger = CoreFunctionService()
        self.dt = datetime.datetime

    async def init_presence(self):
        """
        Change the Bot's Presence to initial message (used in startup on complete).
        :return:
        """
        # Note: Most of the defined items in the Activity seems to not be working
        # Leaving in for now...
        presence = Activity(
            name="Handling Subroutines",
            type=ActivityType.playing,
            assets={
                "large_image": "td1_tea_time-1",
                "small_image": "gbth_vector"
            },
            details="For Help: ~help | !help | ?help | @Sir Top Hat help",
            application_id=797501470844911617,
        )

        presence.application_id = 797501470844911617

        global START_TIME
        START_TIME = time.time()

        await self.change_presence(
            activity=presence
        )

    async def uptime(self, ctx: Context or ApplicationCommandInteraction):
        """
        Returns the uptime of the bot.
        :param ctx:
        :return:
        """
        current_time = time.time()
        embed = Embed(
            title=f"Current Uptime:",
            description=f"`{datetime.timedelta(seconds=round(current_time - START_TIME, 0))}`",
            timestamp=datetime.datetime(
                year=self.dt.now().year,
                month=self.dt.now().month,
                day=self.dt.now().day,
                hour=self.dt.now().hour,
                minute=self.dt.now().minute,
                second=self.dt.now().second
            ),
            colour=0x008369,
        )
        embed.set_footer(text="Showing Uptime")
        embed.set_author(name=self.user, icon_url=self.user.avatar.url)

        await ctx.response.send_message(embed=embed) if hasattr(ctx, "response") else await ctx.send(embed=embed)

    async def msg_presence(self, activity: ActivityType, message: str, status: str):
        """
        Sets a customised presence of the Bot.

        For command method, you should parse it through update_presence().

        :param status: The Status in String that is to be converted into Status Class
        :param activity: The Activity Type in ActivityType
        [playing, listening, watching, streaming, custom, competing]
        :param message: The message itself, in str
        :return:
        """
        presence = Activity(
            name=message,
            type=activity,
            start=datetime.datetime(
                year=self.dt.now().year,
                month=self.dt.now().month,
                day=self.dt.now().day,
                hour=self.dt.now().hour,
                minute=self.dt.now().minute,
                second=self.dt.now().second
            ),
            assets={
                "large_image": "td1_tea_time-1",
                "small_image": "gbth_vector"
            },
            details="For Help: ~help | !help | ?help | @Sir Top Hat help",
            application_id=797501470844911617,
        )

        await self.change_presence(
            activity=presence,
            status=self.get_status(status.lower())
        )

    async def on_ready(self):
        """
        Init Event for Bot.
        :return:
        """
        self.master_logger.info(f"Main Bot Service Started. -> [BOT USER]: {self.user}")

        # Check ServerData
        await on_init(self.guilds)

        # Set Init Presence
        await self.init_presence()

        # Check For Updates
        check_current_version()

        self.master_logger.info(f"Main Init Service Complete.")

    async def on_member_join(self, member: Member):
        """
        Event when a user joins a server.
        :param member: Member
        :return:
        """
        guild: Guild = member.guild

        event_channel: TextChannel = guild.system_channel
        allow_events: bool = get_serverdata_value("allow_events", guild)

        if allow_events is True and event_channel is not None:
            await event_channel.send(f"Mind the Gap between the train and the platform. Welcome, {member.name} to the {get_emoji(self.emojis, '<:GBTHVector:848909712934174764>')} {guild.name} Express.")

    async def on_member_remove(self, member: Member):
        """
        EVent when a member leaves the server.
        :param member: Member
        :return:
        """
        guild: Guild = member.guild

        event_channel: TextChannel = guild.system_channel
        allow_events: bool = get_serverdata_value("allow_events", guild)

        if allow_events is True and event_channel is not None:
            await event_channel.send(f"The train is leaving the station. Goodbye, {member.name}, and thank you for your patronage on the {get_emoji(self.emojis, '<:GBTHVector:848909712934174764>')} {guild.name} Express.")

    @staticmethod
    async def shutdown_bot(ctx: Context or ApplicationCommandInteraction):
        """
        Function to shut down the Bot through non Python Console means.

        :param ctx: Context or ApplicationCommandInteraction
        :return:
        """
        cmd_handler = CommandHandler(
            min_level=CommandHandler.DEVELOPER,
            user_id=ctx.author.id,
            server=ctx.guild
        )

        eligibility = await cmd_handler.check_cmd_req(ctx)

        if eligibility is False:
            return

        await ctx.response.send_message("Shutting down bot...") if hasattr(ctx, "response") else \
            await ctx.send("Shutting down bot...")
        time.sleep(2)
        sys.exit("SHUTDOWN - INITIATED FROM COMMAND")

    @staticmethod
    async def restart_bot(ctx: Context or ApplicationCommandInteraction):
        """
        Function to restart the Bot through non Python Console means.

        :param ctx: Context or ApplicationCommandInteraction
        :return:
            """
        cmd_handler = CommandHandler(
            min_level=CommandHandler.DEVELOPER,
            user_id=ctx.author.id,
            server=ctx.guild
        )

        eligibility = await cmd_handler.check_cmd_req(ctx)

        if eligibility is False:
            return

        await ctx.response.send_message("Restarting bot...") if hasattr(ctx, "response") else \
            await ctx.send("Restarting bot...")
        time.sleep(2)
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])

    async def ping_cmd(self, ctx: Context or ApplicationCommandInteraction):
        """
        Function to report the network latency of the Bot.

        :param ctx: Context or ApplicationCommandInteraction
        :return:
        """
        await ctx.response.send_message(f"Pong! `{round(self.latency * 1000, 2)} ms`") if hasattr(ctx, "response") else \
            await ctx.reply(f"Pong! `{round(self.latency * 1000, 2)} ms`")

    @staticmethod
    async def version(ctx: Context or ApplicationCommandInteraction):
        """
        Function to report the current version of the bot and other modules in the project.

        :param ctx: Context or ApplicationCommandInteraction
        :return:
        """
        await ctx.response.send_message(f"Current Version: {proj_vers} [BOT] | {log_vers} [LOGGER]") if hasattr(ctx, "response") else \
            await ctx.send(f"Current Version: {proj_vers} [BOT] | {log_vers} [LOGGER]")

        await ctx.send(f"[{proj_cpr}] | [{log_cpr}]")

    async def update_presence(self, ctx: Context or ApplicationCommandInteraction, activity: str, status: str, args):
        """
        Command method to update presence. Parses into msg_preference() for lateral execution.

        :param status: Status in string
        :param ctx: Context or ApplicationCommandInteraction
        :param activity: The Activity Type in ActivityType
        [playing, listening, watching, streaming, custom, competing]
        :param args: The message itself, in str
        :return:
        """
        cmd_handler = CommandHandler(
            min_level=CommandHandler.DEVELOPER,
            user_id=ctx.author.id,
            server=ctx.guild
        )

        eligibility = await cmd_handler.check_cmd_req(ctx)

        if eligibility is False:
            return

        await self.msg_presence(self.determine_activity(activity), args, status)

        return await ctx.response.send_message("Presence Updated.") if hasattr(ctx, "response") \
            else await ctx.send("Presence Updated.")

    async def set_init_presence(self, ctx: Context or ApplicationCommandInteraction):
        """
        Command method to set to init presence. Parses into init_presence() for lateral execution.

        :param ctx: Context or ApplicationCommandInteraction
        :return:
        """
        cmd_handler = CommandHandler(
            min_level=CommandHandler.DEVELOPER,
            user_id=ctx.author.id,
            server=ctx.guild
        )

        eligibility = await cmd_handler.check_cmd_req(ctx)

        if eligibility is False:
            return

        await self.init_presence()

        return await ctx.response.send_message("Presence updated.") if hasattr(ctx, "response") \
            else await ctx.send("Presence Updated.")

    @staticmethod
    def determine_activity(activity):
        if activity == "playing":
            return ActivityType.playing
        elif activity == "listening":
            return ActivityType.listening
        elif activity == "streaming":
            return ActivityType.streaming
        elif activity == "watching":
            return ActivityType.watching
        elif activity == "custom":
            return ActivityType.custom
        elif activity == "competing":
            return ActivityType.competing
        else:
            return ActivityType.playing

    @staticmethod
    async def update_serverdata_cmd(ctx: Context or ApplicationCommandInteraction, value: bool):
        cmd_handler = CommandHandler(
            min_level=CommandHandler.SRV_OWNER,
            max_level=CommandHandler.SRV_OWNER,
            server=ctx.guild,
            user_id=ctx.author.id
        )

        eligibility = await cmd_handler.check_cmd_req(ctx)

        if eligibility is False:
            return

        await allowable_events(value, ctx.guild)

        return await ctx.response.send_message(f"Allowable Events for {ctx.guild.name} is set to {value}.") if hasattr(ctx, "response") \
            else await ctx.send(f"Allowable Events for {ctx.guild.name} is set to {value}.")

    @staticmethod
    def get_status(status):
        if status == "online":
            return Status.online
        elif status == "away" or status == "idle":
            return Status.idle
        elif status == "do not disturb" or status == "do_not_disturb" or status == "dnd":
            return Status.dnd
        elif status == "invisible" or status == "invis":
            return Status.invisible
        elif status == "streaming":
            return Status.streaming
        else:
            return Status.online

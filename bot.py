import argparse
import datetime
import disnake
import subprocess
import sys
import os
from disnake import User, CommandInteraction, ApplicationCommandInteraction, Embed, InteractionMessage
from disnake.ext.commands import command, Context, is_owner, guild_only
from dotenv import load_dotenv
from pathlib import Path
from CoFunctions.Paraloop import end_paraloop, end_paraloop_targeted
from MainFunctions.CoreFunction import TD1BotClient
from MainFunctions.DMHandler import dm_cmd, dm_TD1_cmd
from CoFunctions.Interpret_Logger import handle_logfile, interpret_log_base
from UtilLib.CommandLevel import CommandHandler
from UtilLib.DevTools import lookup_dev_cmd
from UtilLib.EmojiHandler import get_emoji
from VersionControl import __version__ as proj_vers, __copyright__ as proj_cpr
from MasterApprenticeLib.TD1_Lib_MasterApprentice_Control import __version__ as log_vers, __copyright__ as log_cpr
from MainFunctions.JSONHandler import JSONHandler

# ======================================================================================================================
# Code Variable Arguments
# Alter variables to alter settings similar that to CMD Args
# REMEMBER TO SET ALL VARIABLES TO FALSE ON PRODUCTION
DEBUG = True  # DEBUG variable to run the bot in Debug mode

# ======================================================================================================================
# ENV Handling
# ENV Path
# Path should be OS friendly to win32, darwin and POSIX OSes
ENV_PATH = os.path.join(Path(__file__).resolve().parent, "Discord_Token.env")

# Load ENV to acquire data
load_dotenv(dotenv_path=ENV_PATH)

# ENV Data Acquirement
# DO NOT DISCLOSE IDs IN CODE. ONLY DISCLOSE IN ENV.
TOKEN = os.getenv("DISCORD_TOKEN")  # Bot Token, Acquirable via DevPortal
DEBUG_TOKEN = os.getenv("DISCORD_DEBUG_TOKEN")  # Secondary Bot Token, Acquirable via DevPortal
BOT_OWNER_ID = int(os.getenv("DEVELOPER_ID"))  # Bot Owner ID, Acquirable via Discord

# ======================================================================================================================
# ArgParse Handling
# Argument CMD Parsing
parser = argparse.ArgumentParser()

# ArgParser Help Desc
parser.description = "A Discord Bot written up by TwelfthDoctor1 that uses the disnake library (originally " \
                     "discord.py) to communicate with the Discord API."

# ArgParser Args
# DEBUG ARGUMENT
parser.add_argument(
    "-d", "--debug",
    help="Start the bot using the DEBUG Account.",
    type=bool, default=False,
    dest="debug"
)
# VERSION ARGUMENT
parser.add_argument(
    "-v", "--ver", "--version",
    help="Show the current version of the bot.",
    action="version",
    version=f"[BOT VERSION]: {proj_vers} | [LOGGER VERSION]: {log_vers}"
)

# Parse CMD Args
# To call argument values, use specified flag name
cmd_args = parser.parse_args()

# Set up Core Args
DEBUG_ARG = cmd_args.debug

# ======================================================================================================================
# Bot Client Init
client = TD1BotClient()


# ======================================================================================================================
# Groups
@client.group(invoke_without_command=True)
async def Developer(ctx: Context):
    await ctx.send("NULL")


# ======================================================================================================================
# Commands List
@client.command()
async def version(ctx: Context):
    return await client.version(ctx)


@client.command()
async def test_type(ctx: Context, *, args):
    async with ctx.channel.typing():
        await ctx.send(args)


@client.command()
async def shutdown(ctx: Context):
    return await client.shutdown_bot(ctx)


@client.command()
async def restart(ctx: Context):
    return await client.restart_bot(ctx)


@client.command("determine_log")
async def interpret_MasApp_log(ctx: Context):
    return await interpret_log_base(ctx)


@client.command()
async def set_init_presence(ctx: Context):
    return await client.set_init_presence(ctx)


@client.command()
async def uptime(ctx: Context):
    return await client.uptime(ctx)


@client.command("set_presence")
async def set_msg_presence(ctx: Context, activity: str, status: str, *, args):
    return await client.update_presence(ctx, activity, status, args)


@client.command()
async def dm(ctx: Context, recipient: User, *, args):
    return await dm_cmd(ctx, recipient, args)


@client.command()
async def dm_TD1(ctx: Context, *, args):
    return await dm_TD1_cmd(ctx, client, args)


@client.command()
async def lookup_dev(ctx: Context):
    return await lookup_dev_cmd(ctx, client)


@client.command()
async def ping(ctx: Context):
    return await client.ping_cmd(ctx)


@client.command()
async def verify(ctx: Context):
    return await ctx.reply(
        "This command is no longer used. Please follow the instructions in the channel to gain access to the server."
    )


@client.command()
async def allowable_events(ctx: Context, value):
    if hasattr(ctx.guild, "id") is False:
        return await ctx.send(f"This command can only be used in servers.")

    return await client.update_serverdata_cmd(ctx, value)


@client.command()
async def emoji_test(ctx: Context, emoji_id):
    emoji = get_emoji(await ctx.guild.fetch_emojis(), emoji_id)
    return await ctx.reply(f"{emoji}")


# ======================================================================================================================
# Slash Commands
@client.slash_command(name="dm", description="Sends a Direct Message to a specified user.")
async def dm_slash(inter: ApplicationCommandInteraction, recipient: User, *, message):
    return await dm_cmd(inter, recipient, message)


@client.slash_command(name="dm_lordpercivalxii", description="Sends a Direct Message to Lord Percival XII.")
async def dm_TD1_slash(inter: ApplicationCommandInteraction, *, message):
    return await dm_TD1_cmd(inter, client, message)


@client.slash_command(name="ping", description="Gets the network latency of the bot.")
async def ping_slash(inter: ApplicationCommandInteraction):
    return await client.ping_cmd(inter)


@client.slash_command(name="shutdown", description="Shutdown the bot through non-Python Console means.")
async def shutdown_slash(inter: ApplicationCommandInteraction):
    return await client.shutdown_bot(inter)


@client.slash_command(name="restart", description="Restart the bot through non-Python Console means.")
async def restart_slash(inter: ApplicationCommandInteraction):
    return await client.restart_bot(inter)


@client.slash_command(name="version", description="Return the current version of the Bot and various modules.")
async def version_slash(inter: ApplicationCommandInteraction):
    return await client.version(inter)


@client.slash_command(name="set_presence", description="Change the presence of the Bot.")
async def update_presence_slash(inter: ApplicationCommandInteraction, activity: str, status: str, *, message):
    return await client.update_presence(inter, activity, status, message)


@client.slash_command(name="set_init_presence", description="Change the presence of the bot to the one used at startup.")
async def init_presence_slash(inter: ApplicationCommandInteraction):
    return await client.set_init_presence(inter)


@client.slash_command(name="uptime", description="Shows the uptime of the bot.")
async def uptime_slash(inter: ApplicationCommandInteraction):
    return await client.uptime(inter)


@client.slash_command(name="allowable_events", description="Determines whether events by the bot should be allowed on the event channel.")
async def allowable_events_slash(inter: ApplicationCommandInteraction, value: bool):
    if hasattr(inter.guild, "id") is False:
        return await inter.response.send_message(f"This command can only be used in servers.")

    return await client.update_serverdata_cmd(inter, value)


@client.slash_command(name="the_end_paradox", description='Create "The end is never the end" statement.')
async def end_paraloop_slash(inter: ApplicationCommandInteraction, cycles: int):
    if cycles <= 0 or cycles > 116:
        cycles = 116

    await end_paraloop(cycles, inter)


@client.slash_command(name="target_the_end_paradox", description='Create "The end is never the end" statement and target onto a user.')
async def target_end_paraloop_slash(inter: ApplicationCommandInteraction, user: User, cycles: int):
    if cycles <= 0 or cycles > 116:
        cycles = 116

    await end_paraloop_targeted(cycles, user, inter)


@client.slash_command(name="ts4_github_repo", description="Returns a list of TD1 TS4 GitHub Repositories")
async def list_ts4_repo_slash(inter: ApplicationCommandInteraction):
    github_json = JSONHandler("TD1TS4GitHubRepo")

    repo_list = github_json.return_json()

    github_embed = Embed(
        title="TD1 TS4 GitHub Repositories",
        description="Listed here is a list of GitHub repositories that is used to store archives, script tutorials and "
                    "script information for TD1 TS4 Mods.",
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

    for repo, repo_data in repo_list.items():
        github_embed.add_field(
            name=repo_data["name"],
            value=f"{repo_data['description']}\n\n"
                  f"-> [View Repository]({repo_data['url']})\n"
        )

    await inter.response.send_message(embed=github_embed)


@client.slash_command(name="td1_github_repo", description="Returns a list of TD1 GitHub Repositories")
async def list_git_repo_slash(inter: ApplicationCommandInteraction):
    github_json = JSONHandler("TD1GitHubRepo")

    repo_list = github_json.return_json()

    github_embed = Embed(
        title="TD1 GitHub Repositories",
        description="Listed here is a list of GitHub repositories that are owned and maintained by TwelfthDoctor1.",
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

    for repo, repo_data in repo_list.items():
        if repo_data['disallow_entry'] is False:
            desc = f"{repo_data['description']}"

            if repo_data['redacted'] is False:
                desc += f"\n\n-> [View Repository]({repo_data['url']})\n"

            github_embed.add_field(
                name=repo_data["name"],
                value=desc
            )

    await inter.response.send_message(embed=github_embed)


@client.slash_command(name="td1_ts4_mods", description="Returns a list of TD1 TS4 Mods")
async def list_td1_ts4_mods_slash(inter: ApplicationCommandInteraction):
    github_json = JSONHandler("TD1ModInfo")

    repo_list = github_json.return_json()

    github_embed = Embed(
        title="TD1 TS4 Mods",
        description="Listed here is a list of TS4 Mods that are owned and maintained by TwelfthDoctor1.\n\n"
                    "Status Notation:\n"
                    "[SUPPORTED] - Mod is currently supported\n"
                    "[UNKNOWN] - Mod is either no longer supported or is in an unknown state",
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

    for repo, repo_data in repo_list.items():
        if repo_data['to_show'] is True:
            desc = f"{repo_data['description']}"

            desc += f"\n\nSTATUS: [{'SUPPORTED' if repo_data['supported'] is True else 'UNKNOWN'}]"

            desc += f"\n\n-> [View Mod]({repo_data['url']})\n"

            github_embed.add_field(
                name=repo_data["name"],
                value=desc,
                inline=True
            )

    await inter.response.send_message(embed=github_embed)


# @client.slash_command(name="set_reminder", description="Set a reminder on the Bot.")
# async def set_reminder_slash(inter: ApplicationCommandInteraction):
#     pass

# @client.slash_command(name="get_arrival_time", description="NULL")
# async def get_bus_arrival_time_slash(inter: ApplicationCommandInteraction):
#     pass



# ======================================================================================================================
# Bot Startup Process
# Initiate Communication with Discord API and connect to Allocated Bot Account specified in DevPortal
# If DEBUG variable or argument is specified, DEBUG account should be used
if DEBUG_ARG is True or DEBUG is True:
    client.run(DEBUG_TOKEN)

else:
    client.run(TOKEN)

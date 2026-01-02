import os
import disnake
from disnake import Attachment, User, ApplicationCommandInteraction
from disnake.ext.commands import Context
from pathlib import Path
import datetime
from MasterApprenticeLib.TD1_Lib_FileHandling import delete_old_logs
from UtilLib.CommandLevel import CommandHandler

LOGGER_ARCHIVE_DIR = Path(os.path.join(Path(__file__).resolve().parent.parent, "UserLogFiles"))


def get_filename(file: Attachment):
    dt = datetime.datetime.now()
    if file.filename.startswith("Master_Log"):
        return f"Master_Log [{dt.day}-{dt.month}-{dt.year}  {dt.hour}:{dt.minute}:{dt.second}]"

    elif file.filename.startswith("Apprentice_Log"):
        return f"Apprentice_Log [{dt.day}-{dt.month}-{dt.year}  {dt.hour}:{dt.minute}:{dt.second}]"

    else:
        return None


def check_for_issue(line):
    if line.startswith("[ERROR"):
        return True

    elif line.startswith("[WARN"):
        return True

    else:
        return False


async def handle_logfile(log_file: Attachment, user: User, ctx: Context or ApplicationCommandInteraction):
    filename = Path(os.path.join(LOGGER_ARCHIVE_DIR, f"{get_filename(log_file)} [{user.id}].log"))
    is_error_sector = False
    encountered_cutoff = True

    error_list = []
    warn_list = []
    debug_lst = []

    # Creation of Blank File for Errno 2 Avoidance
    # temp_file = open(filename, "x")
    # temp_file.close()

    # Directory Exist Check & Creation
    if not os.path.exists(LOGGER_ARCHIVE_DIR):
        os.makedirs(LOGGER_ARCHIVE_DIR)

    await log_file.save(filename)

    with open(filename, "r") as file:
        for line in file.readlines():
            # print(line)

            if check_for_issue(line) is True and encountered_cutoff is True:
                is_error_sector = True
                await ctx.send("Error found in Log File:")
                # print("Error in Log File:\n")
                # await ctx.send(line)
                # print(line)

            elif line.startswith("="):
                encountered_cutoff = True
                is_error_sector = False
                # print(" ")
            elif line.startswith("\n"):
                pass

            else:
                encountered_cutoff = False

            if is_error_sector:
                if line != "\n":
                    #await ctx.responses.send_message(line) if hasattr(ctx, "responses") else \
                    await ctx.send(line)
                    # print(line)


async def interpret_log_base(ctx: Context | ApplicationCommandInteraction):
    async for message in ctx.channel.history(limit=1, oldest_first=False):
        if message.author.id == ctx.author.id and message.content.find("determine_log") != -1:
            msg = message
            break
        else:
            return await ctx.send("Unknown trigger point usage of command.")

    if len(msg.attachments) == 0:
        return await ctx.send(
            "**Please attach a MasterApprentice Log File in the command before sending.** [Files Accepted: Master_Log.log OR Apprentice_Log.log]")

    for file in msg.attachments:
        if file.filename.startswith("Master_Log") is False and file.filename.startswith("Apprentice_Log") is False:
            await ctx.send(
                    f"**The uploaded file [{file.filename}] is NOT a MasterApprentice Log File. Please ensure that the file starts with Master_Log or Apprentice_Log.**")
            continue

        # print(f"The file {file.filename} is a MasterApprentice Log File.")

        await handle_logfile(file, ctx.author, ctx)

    return None


async def delete_old_user_logs(ctx: Context or ApplicationCommandInteraction):
    cmd_handler = CommandHandler(
        min_level=CommandHandler.DEVELOPER,
        user_id=ctx.author.id,
        server=Context.guild
    )

    await cmd_handler.check_cmd_req(ctx)

    delete_old_logs(LOGGER_ARCHIVE_DIR, "Apprentice_Log")
    delete_old_logs(LOGGER_ARCHIVE_DIR, "Master_Log")


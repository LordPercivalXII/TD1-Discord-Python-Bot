import os
import disnake
import json
from disnake import Attachment, User, ApplicationCommandInteraction, Guild
from disnake.ext.commands import Context
from pathlib import Path
from UtilLib.LoggerService import BaseLoggerService
from UtilLib.JSONParser import json_dump, json_load


# Base Structure to reference creation & update of ServerData
SERVER_DATA_STRUCTURE = ["server_guild", "admins", "server_owner", "admin_roles", "allow_events"]

# Structure to disallow tampering of data values for explicit keys - non-specific handling update
SERVER_DATA_CHANGEABLE = [False, False, False, False, True]


class ServerDataHandlerService(BaseLoggerService):
    pass


SERVER_DATA_SERVICE = ServerDataHandlerService()
SERVER_DATA_PATH = Path(os.path.join(Path(__file__).resolve().parent.parent, "ServerData"))


async def on_init(guilds: [Guild]):
    """
    Function to check on ServerData & AdminData on Bot Init.

    Creation of files when file does not exist.
    :param guilds:
    :return:
    """
    # Directory Exist Check & Creation
    if not os.path.exists(SERVER_DATA_PATH):
        os.makedirs(SERVER_DATA_PATH)

    SERVER_DATA_SERVICE.info("Starting ServerData Init Check...")

    for guild in guilds:
        data_file = os.path.join(SERVER_DATA_PATH, f"{guild.id}.json")
        if not os.path.exists(data_file):

            SERVER_DATA_SERVICE.info(f"ServerData Check on [{guild.name}] does not exist in database.\n\nCreating new entry...")

            with open(data_file, "w") as c_data_file:
                server_admins = [guild.owner_id]

                server_data = {
                    "server_guild": guild.id,
                    "admins": server_admins,
                    "server_owner": guild.owner_id,
                    "admin_roles": [],
                    "allow_events": False
                }

                data_json = json_dump(server_data)

                SERVER_DATA_SERVICE.info(f"ServerData on [{guild.name}]:\n\n{data_json}")

                c_data_file.write(data_json)

                c_data_file.close()

            SERVER_DATA_SERVICE.info(f"ServerData Entry on [{guild.name}] recorded into database. Going onto next entry (if any)...")

        else:
            SERVER_DATA_SERVICE.info(f"ServerData Check on [{guild.name}] exists in database. Check data entries...")

            update_count = 0

            with open(data_file, "r") as c_data_file:

                data_dict = json_load(c_data_file.read())

                c_data_file.close()

            for entry in SERVER_DATA_STRUCTURE:
                datacheck = False
                for (k, v) in data_dict.items():
                    if entry == k:
                        datacheck = True
                        break
                    else:
                        datacheck = False

                if not datacheck:
                    data_dict.update({
                        entry: infill_data(entry, guild)
                    })

                    update_count += 1

                    SERVER_DATA_SERVICE.info(f"ServerData missing [{entry}] entry, inserting...")

            if update_count > 0:
                data_json = json_dump(data_dict)

                SERVER_DATA_SERVICE.info(f"Updated ServerData Entry on [{guild.name}]:\n\n{data_json}")

                with open(data_file, "w") as c_data_file:
                    c_data_file.write(data_json)

                    c_data_file.close()

                SERVER_DATA_SERVICE.info(f"ServerData Entry on [{guild.name}] updated. Going onto next entry (if any)...")
            else:
                SERVER_DATA_SERVICE.info(f"ServerData Entry on [{guild.name}] has up-to-date entries. Going onto next entry (if any)...")

    SERVER_DATA_SERVICE.info(f"ServerData Init Check Process Complete. Going onto AdminData Init Check...")

    admin_data_file = os.path.join(SERVER_DATA_PATH, f"AdminData.json")

    if not os.path.exists(admin_data_file):

        SERVER_DATA_SERVICE.info(f"AdminData Check on Entry does not exist. Creating...")

        with open(admin_data_file, "w") as a_data_file:
            admin_data = {
                "admins": []
            }

            admin_data_json = json_dump(admin_data)

            a_data_file.write(admin_data_json)

            a_data_file.close()

    else:
        SERVER_DATA_SERVICE.info(f"AdminData Check on Entry exists.")

    SERVER_DATA_SERVICE.info(f"Full Data Init Check Process Complete.")


def infill_data(key: str, guild: Guild = None):
    if key == "server_guild":
        return guild.id
    elif key == "server_admins":
        return [guild.owner_id]
    elif key == "server_owner":
        return guild.owner_id
    elif key == "admin_roles":
        return []
    elif key == "allow_channel":
        return False
    else:
        return None


def get_serverdata_value(key: str, guild: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{guild.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    for (k, v) in data_dict.items():
        if k == key:
            return v

    return None


def key_value_changeable(key):
    if SERVER_DATA_CHANGEABLE[SERVER_DATA_STRUCTURE.index(key)]:
        return True

    else:
        return False


def update_serverdata_value(key: str, value, guild: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{guild.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    if not key_value_changeable(key):
        return False

    for (k, v) in data_dict.items():
        if k == key:
            data_dict[k] = value

            with open(data_file, "w") as c_data_file:
                data_json = json_dump(data_dict)
                c_data_file.write(data_json)

                c_data_file.close()

            return True

    return False


async def register_srv_admin(user: User, server: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{server.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    if user.id == data_dict["server_owner"]:
        return False

    for admin in data_dict["admins"]:
        if admin == user.id:
            return False

    data_dict["admins"].append(user.id)

    with open(data_file, "w") as c_data_file:
        data_json = json_dump(data_dict)
        c_data_file.write(data_json)

        c_data_file.close()

    return True


async def deregister_srv_admin(user: User, server: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{server.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    if user.id == data_dict["server_owner"]:
        return False

    for admin in data_dict["admins"]:
        if admin == user.id:
            data_dict["admins"].remove(user.id)

            with open(data_file, "w") as c_data_file:
                data_json = json_dump(data_dict)
                c_data_file.write(data_json)

                c_data_file.close()

            return True

    return False


def acquire_data(key: str, server: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{server.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    for (k, v) in data_dict.items():
        if k == key:
            return data_dict[key]

    return None


async def register_admin(user: User):
    from bot import BOT_OWNER_ID

    admin_data_file = os.path.join(SERVER_DATA_PATH, f"AdminData.json")

    with open(admin_data_file, "r") as a_data_file:
        data_dict = json_load(a_data_file.read())

        a_data_file.close()

    if user.id == BOT_OWNER_ID:
        return False

    for (k, v) in data_dict.items():
        if v == user.id:
            return False

    data_dict["admins"].append(user.id)

    with open(admin_data_file, "w") as c_data_file:
        data_json = json_dump(data_dict)
        c_data_file.write(data_json)

        c_data_file.close()

    return True


async def deregister_admin(user: User):
    from bot import BOT_OWNER_ID

    admin_data_file = os.path.join(SERVER_DATA_PATH, f"AdminData.json")

    with open(admin_data_file, "r") as a_data_file:
        data_dict = json_load(a_data_file.read())

        a_data_file.close()

    if user.id == BOT_OWNER_ID:
        return False

    for (k, v) in data_dict.items():
        if v == user.id:
            data_dict["admins"].remove(user.id)

            with open(admin_data_file, "w") as c_data_file:
                data_json = json_dump(data_dict)
                c_data_file.write(data_json)

                c_data_file.close()

            return True

    return False


def acquire_admin(user: int):
    admin_data_file = os.path.join(SERVER_DATA_PATH, f"AdminData.json")

    with open(admin_data_file, "r") as a_data_file:
        data_dict = json_load(a_data_file.read())

        a_data_file.close()

    for (k, v) in data_dict.items():
        if v == user:
            return True

    return False


async def allowable_events(value: bool, server: Guild):
    data_file = os.path.join(SERVER_DATA_PATH, f"{server.id}.json")

    with open(data_file, "r") as c_data_file:
        data_dict = json_load(c_data_file.read())

        c_data_file.close()

    data_dict["allow_events"] = value

    with open(data_file, "w") as c_data_file:
        data_json = json_dump(data_dict)
        c_data_file.write(data_json)

        c_data_file.close()

    return True

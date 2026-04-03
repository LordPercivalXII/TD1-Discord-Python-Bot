import os
from disnake import User, Guild
from pathlib import Path
from UtilLib.JSONHandler import JSONHandler
from UtilLib.LoggerService import BaseLoggerService


# Base Structure to reference ServerData to disallow tampering of data values for explicit keys - non-specific handling update
SERVER_DATA_CHANGEABLE_STRUCTURE = {
    "server_guild": False,
    "admins": False,
    "server_owner" : False,
    "admin_roles": False,
    "allow_events": True
}


class ServerDataHandlerService(BaseLoggerService):
    pass


SERVER_DATA_PATH = Path(os.path.join(Path(__file__).resolve().parent.parent, "ServerData"))


class ServerDataHandler:
    def __init__(self):
        self.admin_data = None
        self.logger = ServerDataHandlerService()
        self.server_data_ref: dict[str, JSONHandler] = dict()

    async def on_init(self, guilds: list[Guild]):
        """
        Function to check on ServerData & AdminData on Bot Init.

        Creation of files when file does not exist.
        :param guilds:
        :return:
        """
        # Directory Exist Check & Creation
        if not os.path.exists(SERVER_DATA_PATH):
            os.makedirs(SERVER_DATA_PATH)

        self.logger.info("Starting ServerData Init Check...")

        # Server (Guild) Data Check
        for guild in guilds:
            guild_json = JSONHandler(str(guild.id), SERVER_DATA_PATH, False)

            self.logger.info(
                f"ServerData Check on [{guild.name}]... (Please check logs for KV check state)"
            )

            server_data_struct = {
                "server_guild": guild.id,
                "admins": [guild.owner_id],
                "server_owner": guild.owner_id,
                "admin_roles": [],
                "allow_events": False
            }

            guild_json.check_json(server_data_struct)

            self.server_data_ref[str(guild.id)] = guild_json

            self.logger.info(f"ServerData Entry on [{guild.name}] complete. Going onto next entry (if any)...")

        self.logger.info(f"ServerData Init Check Process Complete. Going onto AdminData Init Check...")

        # Bot Admin Check
        self.admin_data = JSONHandler("AdminData", SERVER_DATA_PATH, False)

        admin_data_struct = {
            "admins": []
        }

        self.admin_data.check_json(admin_data_struct)

        self.logger.info(f"AdminData Check on Entry exists.")

        self.logger.info(f"Full Data Init Check Process Complete.")

    @staticmethod
    def infill_data(key: str, guild: Guild):
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

    def get_serverdata_value(self, key: str, guild: Guild):
        guild_json = self.server_data_ref[str(guild.id)]
        return guild_json.return_specific_json(key)

    @staticmethod
    def key_value_changeable(key):
        return SERVER_DATA_CHANGEABLE_STRUCTURE[key]

    def update_serverdata_value(self, key: str, value, guild: Guild):
        if not self.key_value_changeable(key):
            return False

        guild_json = self.server_data_ref[str(guild.id)]
        guild_json.update_specific_json(key, value)
        guild_json.update_json_file()

        return True

    async def register_srv_admin(self, user: User, guild: Guild):
        guild_json = self.server_data_ref[str(guild.id)]

        if user.id == guild_json.return_specific_json("server_owner"):
            return False

        admin_list: list = guild_json.return_specific_json("admins")

        if user.id in admin_list:
            return False

        admin_list.append(user.id)

        guild_json.update_specific_json("admins", admin_list)
        guild_json.update_json_file()

        return True

    async def deregister_srv_admin(self, user: User, guild: Guild):
        guild_json = self.server_data_ref[str(guild.id)]

        if user.id == guild_json.return_specific_json("server_owner"):
            return False

        admin_list: list = guild_json.return_specific_json("admins")

        if user.id in admin_list:
            admin_list.remove(user.id)

            guild_json.update_specific_json("admins", admin_list)
            guild_json.update_json_file()

            return True

        return False

    async def register_admin(self, user: User):
        from bot import BOT_OWNER_ID

        if user.id == BOT_OWNER_ID:
            return False

        admin_data_list: list = self.admin_data.return_specific_json("admins")

        if user.id in admin_data_list:
            return False

        admin_data_list.append(user.id)

        self.admin_data.update_json("admins", admin_data_list)
        self.admin_data.update_json_file()

        return True

    async def deregister_admin(self, user: User):
        from bot import BOT_OWNER_ID

        if user.id == BOT_OWNER_ID:
            return False

        admin_data_list: list = self.admin_data.return_specific_json("admins")

        if user.id in admin_data_list:
            admin_data_list.remove(user.id)

            self.admin_data.update_json("admins", admin_data_list)
            self.admin_data.update_json_file()

            return True

        return False

    def acquire_admin(self, user: int):
        return user in self.admin_data.return_specific_json("admins")

    async def allowable_events(self, value: bool, guild: Guild):
        guild_json = self.server_data_ref[str(guild.id)]

        guild_json.update_specific_json("allow_events", value)
        guild_json.update_json_file()

        return True

    def get_servers(self):
        return list(int(k) for k in self.server_data_ref.keys())

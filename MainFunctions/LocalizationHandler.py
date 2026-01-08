import os
import urllib.request
import urllib.error
import enum
from pathlib import Path
from UtilLib.JSONParser import json_load
from UtilLib.LoggerService import LoggerClass


class StringHandlerService(LoggerClass):
    def __init__(self):
        super(StringHandlerService, self).__init__(
            module_name=f"TD1 Python Bot | {self.__class__.__name__}",
            main_owner="TwelfthDoctor1",
            log_enable=False,
            mlog_enable=True
        )


STRING_LIB = os.path.join(Path(__file__).resolve().parent.parent, "StringLib")
BASE_URL = "https://raw.githubusercontent.com/TwelfthDoctor1/TD1-Discord-Python-Bot/main/StringLib/"
STRINGHANDLER_SERVICE = StringHandlerService()


class LocalizedStringEnum(enum):
    """
    Enums used to determine the String to used based on Localization.
    """
    ENG_US_UK = 0


class LocalizationHandler:
    def __init__(self, str_type: LocalizedStringEnum, str_id: int, fallback_str: str, use_git: bool = False):
        """
        Initialise LocalizationHandler to handle Localized Strings based from numerical IDs.
        :param str_type: The attribute name
        :param str_id:
        """
        self.str_id = str_id
        self.str_type = str_type
        self.fallback_str = fallback_str
        self.use_git = use_git

    def get_localized_str_from_id(self):
        data_path = os.path.join(STRING_LIB, self.convert_enum_into_str_fp())

        if os.path.exists(data_path) is False:
            return self.fallback_str

        pass

    def formulate_str_data_from_json(self, fp):
        def offline_formulation():
            with open(fp, "r") as json_ref:
                self.str_data = json_load(json_ref.read())
                json_ref.close()

            return True

        def online_formulation():
            json_url = BASE_URL + self.convert_enum_into_str_fp()
            json_req = urllib.request.Request(url=json_url, method="GET")

            try:
                with urllib.request.urlopen(json_req) as response:
                    self.json_data = json_load(response.read().decode("utf-8"))

                    return True

            except urllib.error.URLError as e:
                STRINGHANDLER_SERVICE.error(
                    f"[FAILURE IN GETTING VERSION IN GITHUB] Either the associated URL is invalid or that the data is "
                    f"not raw or may be caused by other issues."
                    f"\nPerhaps Check your internet connection?"
                )

                if hasattr(e, "code") and hasattr(e, "reason"):
                    # HTTP Error Code + Reason
                    STRINGHANDLER_SERVICE.error(f"HTTP ERROR CODE {e.code} | {e.reason}")

                elif hasattr(e, "reason"):
                    # HTTP Error Reason
                    STRINGHANDLER_SERVICE.error(f"FAILURE REASON | {e.reason}")

                else:
                    # Exception Error Dump
                    STRINGHANDLER_SERVICE.error(f"RAW FAILURE REASON | {e}")

                return False

        if self.use_git is False:
            offline_formulation()

        can_acquire = online_formulation()

        if can_acquire is False:
            offline_formulation()

    def convert_enum_into_str_fp(self):
        # Language: English
        if self.str_type == LocalizedStringEnum.ENG_US_UK:
            return "lang_eng.json"
        # Append more languages below

        # Fallback Usage - English
        else:
            return "lang_eng.json"


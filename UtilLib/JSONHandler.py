import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from UtilLib.LoggerService import BaseLoggerService


class JSONHandlerService(BaseLoggerService):
    pass


JSON_LIB = os.path.join(Path(__file__).resolve().parent.parent, "JSONLib")
BASE_URL = "https://raw.githubusercontent.com/LordPercivalXII/TD1-Discord-Python-Bot/main/JSONLib/"


class JSONHandler:
    """
    JSONHandler

    A class that is able to acquire JSON data from GitHub or from JSONLib.
    """
    def __init__(self, json_data_name: str, json_dir: Path | str = "", json_use_git: bool = False):
        """
        Initialise JSONHandler to acquire data.
        :param json_data_name: Name of JSON File, with .json suffix
        :param json_use_git: Whether JSON Data should be acquired Online or Offline
        """
        self.logger = JSONHandlerService()
        self.json = json_data_name
        self.json_data: dict = dict()
        self.git_use: bool = json_use_git
        self.json_dir = json_dir
        self.json_fp = os.path.join(self.json_dir, self.json + ".json") if self.json_dir != "" \
            else os.path.join(JSON_LIB, self.json + ".json")

        # Formulate JSON -> Acquire Data from Provided Values
        self.formulate_json()

    def formulate_json(self):
        def offline_formulation():
            print("OFFLINE FORMULATION")
            with open(self.json_fp, "r") as json_ref:
                self.json_data = self.json_load(json_ref.read())
                json_ref.close()

            self.logger.info(
                "Formulated & ascertained JSON File Data. Data can now be acquired/set with get/set functions.",
                to_console=False
            )

            return True

        def online_formulation():
            print("ONLINE FORMULATION")
            json_url = BASE_URL + self.json + ".json"
            json_req = urllib.request.Request(url=json_url, method="GET")

            try:
                with urllib.request.urlopen(json_req) as response:
                    self.json_data = self.json_load(response.read().decode("utf-8"))

                self.logger.info(
                    "Formulated & ascertained JSON File Data. Data can now be acquired/set with get/set functions.",
                    to_console=False
                )

                return True

            except urllib.error.URLError as e:
                self.logger.error(
                    f"[FAILURE IN GETTING VERSION IN GITHUB] Either the associated URL is invalid or that the data is "
                    f"not raw or may be caused by other issues."
                    f"\nPerhaps Check your internet connection?"
                )

                if hasattr(e, "code") and hasattr(e, "reason"):
                    # HTTP Error Code + Reason
                    self.logger.error(f"HTTP ERROR CODE {e.code} | {e.reason}")

                elif hasattr(e, "reason"):
                    # HTTP Error Reason
                    self.logger.error(f"FAILURE REASON | {e.reason}")

                else:
                    # Exception Error Dump
                    self.logger.error(f"RAW FAILURE REASON | {e}")

                return False

        if not self.git_use:
            return offline_formulation()

        can_acquire = online_formulation()

        if not can_acquire:
            return offline_formulation()
        else:
            return can_acquire

    def generate_json(self, data_dict: dict):
        """
        Generate the JSON File should the JSON File not exist.
        If the file exists, it will be skipped.

        :param data_dict: Data in Dictionary Form
        :return:
        """
        if not os.path.exists(self.json_fp):

            self.logger.info(
                f"JSON File ({self.json}) does not exist. Creating...",
                to_console=False
            )

            with open(self.json_fp, "w") as json_file:
                json_file.write(self.json_dump(data_dict))
                json_file.close()

            return True
        else:
            self.logger.info(
                f"JSON File ({self.json}) already exists. Skipping...",
                to_console=False
            )
            return False

    def check_json(self, data_dict: dict):
        """
        Generate the Config JSON. Avoids usage of generate_json().
        * This function derives from ConfigJSON, of which has no use case here.
        :return:
        """
        status = self.generate_json(data_dict)
        self.generate_json(data_dict)

        # Key Check on Existing Config
        if not status:
            # key_check_list = list(self.json_data.keys())
            missing_keys = []
            for key_def in data_dict.keys():
                has_checked = False
                # for key_check in key_check_list:
                if key_def in self.json_data:
                    if self.logger is not None:
                        self.logger.debug(f"DEBUG: CHECK -> {key_def}")
                    # key_check_list.remove(key_check)
                    has_checked = True

                if not has_checked:
                    missing_keys.append(key_def)

            if self.logger is not None:
                self.logger.debug(f"DEBUG: KEY CHECK MISSING {len(missing_keys)} "
                                  f"KEYS: {missing_keys if len(missing_keys) > 0 else None}")

            # Add missing keys
            if len(missing_keys) > 0:
                if self.logger is not None:
                    self.logger.info(f"Config Check: {len(missing_keys)} keys missing. Appending...\n\n{missing_keys}")

                for key in missing_keys:
                    self.json_data[key] = data_dict[key]

                # Update File for future reads
                self.update_json_file()
                if self.logger is not None:
                    self.logger.info(f"Config Check: Updated JSON File {self.json_fp}")
            else:
                if self.logger is not None:
                    self.logger.info(f"Config Check: All keys accounted for. No key appending required.")

    def update_json_file(self):
        """
        Update the JSON File to include the changed entries in self.json_data.
        :return:
        """
        with open(self.json_fp, "w") as json_file:
            # print(json_dump(self.json_data))
            json_file.write(self.json_dump(self.json_data))
            json_file.close()

        self.logger.info(
            "JSON File has been updated. All previous data entries have been overridden.",
            to_console=False
        )

    def return_json(self):
        """
        Return the JSON in dictionary form.
        :return:
        """
        return self.json_data

    def return_specific_json(self, key: str):
        """
        Return the specific value by referencing to a key.
        :param key: Dictionary Key
        :return:
        """
        return self.json_data[key]

    def update_json(self, data_dict: dict):
        """
        Update the entire JSON Dictionary entry.
        :param data_dict: Dictionary Data
        :return:
        """
        self.json_data = data_dict

    def update_specific_json(self, key: str, value):
        """
        Update a specific JSON Data value.
        :param key: Dictionary Key
        :param value: Dictionary Value
        :return:
        """
        self.json_data[key] = value

    def add_json_entry(self, key: str = None, value=None, dict_data: dict = None):
        """
        Add a new JSON Entry.

        Either add using Key Value or by Dictionary.
        :param key: Dictionary Key
        :param value: Dictionary Value
        :param dict_data: Dictionary Data
        :return:
        """
        if key is not None and value is not None:
            self.json_data[key] = value
        else:
            self.json_data.update(dict_data)

    def delete_json_entry(self, key: str):
        """
        Delete a JSON Entry.
        :param key: Dictionary Key
        :return:
        """
        del self.json_data[key]

    @staticmethod
    def json_dump(json_dict: dict):
        """
        Function to convert Python Dictionary into JSON.
        :param json_dict: Dictionary to be converted into JSON format.
        :return:
        """
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @staticmethod
    def json_load(json_data: str | bytes):
        """
        Function to convert JSON into Python Dictionary.
        :param json_data: JSON data to be converted into Dictionary format.
        :return:
        """
        return json.loads(json_data)


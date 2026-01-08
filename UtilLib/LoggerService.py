import enum
import datetime
from warnings import warn
from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger


class LoggingLevel(enum.IntEnum):
    """
    LoggingLevel is an enum class used to determine the logging level of the logging activity.
    Alternatively, they can be used for other cases such as testing for specific levels, etc.

    Levels are sorted in terms of their priority.

    """
    DEBUG = -2
    LOG = -1
    NONE = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    ASSERT_ERROR = 4
    EXCEPTION = 5


class LoggerClass(ApprenticeLogger):
    """
    A dual function Logger cloning ApprenticeLogger & MasterLogger

    self - ApprenticeLogger Class and Functions
    self.mlog - MasterLogger Class and Functions

    Modified to include logging to console.
    """

    def __init__(self, module_name=None, main_owner=None, additional_context=None, log_enable=True, mlog_enable=False):
        super(LoggerClass, self).__init__(
            module_name=module_name,
            main_owner=main_owner,
            additional_context=additional_context,
            enable=log_enable
        )
        self.mlog = MasterLogger(
            module_name=module_name,
            main_owner=main_owner,
            additional_context=additional_context,
            enable=mlog_enable
        )
        self.info(f"File creation of Log at: {self.get_log_dir()}")
        self.mlog.info(f"File creation of Log at: {self.mlog.get_log_dir()}")

    def info(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).info(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.info(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def log(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).log(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.log(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def debug(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        if to_apprentice:
            super(LoggerClass, self).debug(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.debug(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            print(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def warn(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).warn(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.warn(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def error(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).error(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.error(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def assert_error(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).assert_error(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.assert_error(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def exception(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True):
        if to_apprentice:
            super(LoggerClass, self).exception(
                message=message,
                owner=owner
            )

        if to_master:
            self.mlog.exception(
                message=message,
                owner=owner
            )

        if to_console:
            dt = datetime.datetime.now()
            warn(f"[{dt.day} {dt.strftime('%B')} {dt.year} | {dt.strftime('%I')}:{dt.strftime('%M')}:{dt.strftime('%S')} {dt.strftime('%p')}"
                  f" | {self.module_name}] {message}")
            print("==============================================================================================================")

    def log_level(self, message, owner=None, to_console=True, to_master=False, to_apprentice=True, level: LoggingLevel = LoggingLevel.INFO):
        if level == LoggingLevel.DEBUG:
            self.debug(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.LOG:
            self.log(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.INFO:
            self.info(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.WARN:
            self.warn(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.ERROR:
            self.error(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.ASSERT_ERROR:
            self.assert_error(message, owner, to_console, to_master, to_apprentice)
        elif level == LoggingLevel.EXCEPTION:
            self.exception(message, owner, to_console, to_master, to_apprentice)

    @property
    def get_service_name(self):
        return self.__class__.__name__


class BaseLoggerService(LoggerClass):
    def __init__(self):
        super(BaseLoggerService, self).__init__(
            module_name=f"TD1 Python Bot | {self.__class__.__name__}",
            main_owner="TwelfthDoctor1",
            log_enable=False,
            mlog_enable=True
        )

    def info(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).info(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def log(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).log(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def debug(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).debug(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def warn(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).warn(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def error(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).error(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def assert_error(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).assert_error(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def exception(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False):
        super(BaseLoggerService, self).exception(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice
        )

    def log_level(self, message, owner=None, to_console=True, to_master=True, to_apprentice=False, level: LoggingLevel = LoggingLevel.INFO):
        super(BaseLoggerService, self).log_level(
            message=message,
            owner=owner,
            to_console=to_console,
            to_master=to_master,
            to_apprentice=to_apprentice,
            level=level
        )
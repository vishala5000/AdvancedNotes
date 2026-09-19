import os


APP_NAME = "Advanced Notes"
APP_VERSION = "1.0.0"

APP_DIRECTORY_NAME = "AdvancedNotes"

DATABASE_FILENAME = "notes.db"

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 700

MIN_PASSWORD_LENGTH = 6
MAX_USERNAME_LENGTH = 50
MAX_NOTE_TITLE_LENGTH = 200

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_app_directory():
    """
    Persistent per-user application directory.

    Example:
    C:\\Users\\Username\\AppData\\Roaming\\AdvancedNotes
    """

    appdata = os.environ.get("APPDATA")

    if not appdata:
        appdata = os.path.expanduser("~")

    directory = os.path.join(
        appdata,
        APP_DIRECTORY_NAME
    )

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def get_database_path():
    return os.path.join(
        get_app_directory(),
        DATABASE_FILENAME
    )

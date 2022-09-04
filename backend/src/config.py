import datetime
import tempfile
import time
import cv2

from services.event import Event


class AppConfig:

    PROJECT_NAME: str = 'Nyo Smart'

    """
    Supply project email here, used for sending email
    """
    PROJECT_EMAIL: str = ""
    """
    Kairos APP ID
    """
    APP_ID: str = None

    """
    Kairos APP KEY
    """
    APP_KEY: str = None

    """
    Kairos API Domain
    """
    API_DOMAIN: str = None

    """
    Initialization Seconds to allow time for Gaussian mixture model to learn the background and foreground
    """
    MOTION_INIT_SEC: int = 60

    """
    Recording File prefix
    """
    FILE_PREFIX: str = "Motion-"


    """
    Directory for uploaded content
    """
    UPLOAD_DIR: str = 'files/upload/'

    """
    Video container
    """
    FOURCC: int = cv2.VideoWriter_fourcc(*"MJPG")

    """
    Host included in notification messages
    """
    HOST_NAME = 'http://192.168.1.12:5050/'

    """
    Video Extension
    """
    EXTENSION: str = 'mp4'

    """
    Should video be colored
    """
    VIDEO_COLORED: bool = True

    """
    Break in each motion before file is saved and motion concluded to have finished
    """
    TILL_RECORD: int = 30

    """
    Size of the object to be detected by the motion detection
    """
    OBJECT_AREA: int = 5000

    """
    Default devices, these devices must be registered
    """
    DEFAULT_DEVICE = {
        'DOOR_CAMERA': 'Door Camera',
        'MOTION_CAMERA': 'Motion Camera',
        'DOOR': 'Door Lock',
        'HTTP_DEVICE': 'Http Device'
    }

    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Dictator@@@123',
        'db': 'final_project',
        'cursor_class': 'DictCursor'
    }

    """
    Mailchimp API key
    """
    MAILCHIMP_KEY = ""

    """
    Grab a secret at checkmobi.com
    """
    CHECKMOBIL_SECRET = ""

    CHECKMBOBI_DOMAIN = "https://api.checkmobi.com/v1"

    """
    Token Secret for login and authorization
    """
    AUTH_TOKEN_SECRET = "SaltSalt33"

    WEBHOOK_TOKEN = "!ht^E6Wp!G6Dm@tIfCa2A4GSKz6JF"

    CURRENT_USER = set()

    TABLES = {
        "LOG": 'log',
        'WEBHOOK': 'webhook',
        'USER': 'user',
        'ALARM': 'alarm'
    }

    event: Event = None

    """
    Initialize with secrets (API etc)
    """
    def __init__(self, domain: str, app_id: str, app_key: str):
        self.APP_KEY = app_key
        self.APP_ID = app_id
        self.API_DOMAIN = domain

    @property
    def registered_devices(self):
        f"""
        Register new devices
        ::return:
        """
        return []

    @property
    def image_name_timer(self):
        return f"enrollment-{datetime.datetime.now().__str__()}-{time.time().__str__()}.jpg"

    @property
    def temp_directory(self):
        return tempfile.mkdtemp()

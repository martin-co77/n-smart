from config import AppConfig
from devices.HttpDevice import HttpDevice
from devices.camera import Camera
from devices.door import Door
from helpers.event_helper import EventHelper
from routes.route import Route
from services.alarm import Alarm
from services.devices import Devices
from flask import Flask
from flask_cors import CORS
from lib.mysql import MySQL
from services.event import Event
from services.motion import MotionDetection
from services.recorder import Recorder
import threading

class Main:
    app_config = None
    db: MySQL = None
    event: Event = None
    daemons = None
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    def __init__(self):
        """
        Second arg is APP ID from kairos.com
        Third arg is the APP KEY from kairos.com
        """
        self.app_config = AppConfig(
            "https://api.kairos.com",
            "",
            ""
        )
        self.db = MySQL(self.app, self.app_config)
        self.devices = Devices()
        self.event = Event()
        self.daemons = []

    def default_devices(self):
        print('default devices')
        self.devices.add_device(
            Camera(
                name=AppConfig.DEFAULT_DEVICE['DOOR_CAMERA'],
                configuration=self.app_config,
                device_url='rtsp://192.168.1.136/live/ch00_1'
            )
        )
        self.devices.add_device(
            Camera(
                name=AppConfig.DEFAULT_DEVICE['MOTION_CAMERA'],
                configuration=self.app_config,
                device_url='rtsp://192.168.1.137/live/ch00_1'
            )
        )
        self.devices.add_device(
            Door(
                name=AppConfig.DEFAULT_DEVICE['DOOR'],
                configuration=self.app_config
            )
        )
        self.devices.add_device(
            HttpDevice(
                name=AppConfig.DEFAULT_DEVICE['HTTP_DEVICE'],
                configuration=self.app_config
            )
        )

    def init_route(self):
        rte = Route(
            self.app_config,
            self.app,
            self.db,
            devices=self.devices
        )
        rte.setup()

    def register_event(self):
        event_helper = EventHelper(self.app_config, self.db, self.devices)
        self.event.register('authorize', lambda x: event_helper.facial_event_recognizer())
        self.event.register('log', lambda x: event_helper.insert_log(x))
        self.event.register('speech', lambda x: event_helper.trigger_speech(x))
        self.app_config.event = self.event

    def init_services(self):
        recorder = Recorder(self.app_config)
        alarm = Alarm(
            configuration=self.app_config,
            db=self.db
        )
        motion_detection_daemon = MotionDetection(
            recorder=recorder,
            configuration=self.app_config,
            alarm=alarm,
            devices=self.devices
        )
        self.daemons.append(motion_detection_daemon)

    def init_devices(self):
        self.default_devices()
        for device in self.app_config.registered_devices:
            self.devices.add_device(device)

    def post_run(self):
        self.init_devices()
        self.init_services()
        self.register_event()
        self.init_route()
        for device in self.devices.all:
            threading.Thread(target=device.run).start()

        for daemon in self.daemons:
            threading.Thread(target=daemon.start).start()

    def run(self):
        self.post_run()
        self.app.run('0.0.0.0', 5050, True, True, use_reloader=False)


if __name__ == "__main__":
    main = Main()
    main.run()

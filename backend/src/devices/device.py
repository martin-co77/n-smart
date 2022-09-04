from config import AppConfig
from exception.device import DeviceException
from lib.request import Request
from system import System


class Device(System):
    name: str = None
    configuration: AppConfig = None
    data = None

    on_timer = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs is None or 'name' not in kwargs:
            raise DeviceException('Device name is required!', [])

        if kwargs is None or 'configuration' not in kwargs:
            raise DeviceException('Configuration file for device is required', [])

        self.on_timer = lambda x: x
        self.name = kwargs['name']

    def initialize(self, nodes=None):
        ...

    def shutdown(self, nodes=None):
        ...

    def run(self, callback=lambda x: x):
        ...

    def get_data(self):
        return self.data

    @staticmethod
    def communicate(configuration, url: str, data):
        request = Request(configuration)
        return request.post(url, data)



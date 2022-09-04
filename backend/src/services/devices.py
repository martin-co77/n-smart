from devices.device import Device
from exception.device import DeviceException


class Devices:
    _device = None

    def __init__(self):
        """
        Provide functionality to add the device
        """
        self._devices = []

    def get_device(self, name: str):
        f"""
        :param name:
        :return {Device}:
        """
        for device in self._devices:
            if device.name == name:
                return device

        raise DeviceException(f"Device with name {name} not found!", [])

    def add_device(self, device: Device):
        """
        :param device:
        :return:
        """
        self._devices.append(device)

    @property
    def all(self):
        return self._devices

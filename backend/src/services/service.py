from exception.not_found import NotFoundException
from services.recorder import Recorder
from system import System


class Service(System):

    """
    Recorder
    """
    recorder: Recorder = None

    def __init__(self, *args, **kwargs):
        if kwargs is None or 'configuration' not in kwargs:
            raise NotFoundException('Configuration is required for service')

        if kwargs is None or 'devices' not in kwargs:
            raise NotFoundException('Devices is required for service')

        if kwargs is not None and 'db' in kwargs:
            self.db = kwargs['db']

        if kwargs is not None and 'recorder' in kwargs:
            self.recorder = kwargs['recorder']

        super().__init__(*args, **kwargs)

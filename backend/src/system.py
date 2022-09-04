from datetime import datetime

from config import AppConfig
from helpers.Log import Log
from lib.mysql import MySQL


class System:
    configuration: AppConfig = None
    db: MySQL = None
    devices= None
    TABLE_NAME: str = None

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        if kwargs is not None and 'configuration' in kwargs:
            self.configuration = kwargs['configuration']

        if kwargs is not None and 'devices' in kwargs:
            self.devices = kwargs['devices']

        if kwargs is not None and 'db' in kwargs:
            self.db = kwargs['db']

    def write_log(self,
                  event_type: str,
                  destination: str,
                  origin: str,
                  msg: str,
                  event_id: int,
                  user_id: int,
                  status=False):
        """
        :param event_type:
        :param destination:
        :param origin:
        :param msg:
        :param event_id:
        :param user:
        :param status:
        :return:
        """

        log = Log(
            type=event_type,
            created_at=datetime.now(),
            destination=destination,
            origin=origin,
            msg=msg,
            log_event_id=event_id,
            user_associated=user_id,
            status=status
        )
        self.configuration.event.call('log', data=log)


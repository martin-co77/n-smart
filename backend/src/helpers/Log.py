import datetime

from exception.invalid_log_input import InvalidLogInput


class Log:
    TABLE: str = 'log'
    LOG_TYPES = {
        'WEBHOOK': 'webhook',
        'RECENT_USER': 'recent_user',
        "RECENT_LOGIN": 'recent_login',
        "INTRUSION": 'intrusion'
    }

    type: str
    created_at: datetime.datetime
    destination: str
    origin: str
    msg: str
    log_event_id: int
    user_associated: int
    status: bool

    def __init__(self, **kwargs):

        if kwargs is None:
            raise InvalidLogInput("No log information was provided")

        if 'type' not in kwargs:
            raise InvalidLogInput('Type is required for log')

        if 'destination' not in kwargs:
            raise InvalidLogInput('destination is required for log')

        if 'origin' not in kwargs:
            raise InvalidLogInput('Origin is required for log')

        if 'msg' not in kwargs:
            raise InvalidLogInput('Message is required for log')

        if 'log_event_id' not in kwargs:
            raise InvalidLogInput('Provide the ID of the element affected by this log. log_event_id is required')

        if 'user_associated' not in kwargs:
            raise InvalidLogInput('User associated is required for log')

        if 'status' not in kwargs:
            raise InvalidLogInput('Status is required for log')

        self.type = self.LOG_TYPES.get(kwargs.get('type'))
        if type is None:
            raise InvalidLogInput('Invalid type provided for log')

        self.created_at = datetime.datetime.now()
        self.destination = kwargs.get('destination')
        self.origin = kwargs.get('origin')
        self.msg = kwargs.get('msg')
        self.log_event_id = kwargs.get('log_event_id')
        self.user_associated = kwargs.get('user_associated')
        self.status = kwargs.get('status')

    @property
    def get_values(self):
        return {
            'type': self.type,
            'created_at': self.created_at,
            'destination': self.destination,
            'origin': self.origin,
            'msg': self.msg,
            'log_event_id': self.log_event_id,
            'user_associated': self.user_associated,
            'status': self.status
        }

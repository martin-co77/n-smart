from exception.not_found import NotFoundException


class Event:
    events = None
    NAMES = {
        'intruder': 'intruder',
        'authorize': 'authorize',
        'speech': 'speech',
        'motion': 'motion',
        'user': 'user',
        'log': 'log'
    }

    def __init__(self):
        self.events = []

    def register(self, name: str, func = lambda x: x):
        self.events.append({'name': name, 'func': func})

    def call(self, name, **kwargs):
        if name not in self.NAMES:
            raise NotFoundException(f"Event {name} not available")

        for item in self.events:
            if item.get('name') == name and callable(item.get('func')):
                item.get('func')(kwargs)

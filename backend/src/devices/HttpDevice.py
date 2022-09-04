from devices.device import Device


class HttpDevice(Device):
    _on_event_type: str = 'Device On'
    _off_event_type: str = 'Device Off'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs is not None and 'on_type' in kwargs:
            self._on_event_type = kwargs['on_type']

        if kwargs is not None and 'off_type' in kwargs:
            self._off_event_type = kwargs['off_type']

    def initialize(self, nodes=None):
        for node in nodes:
            self.write_log(
                'WEBHOOK',
                node.get('url', None),
                self.name,
                self._on_event_type,
                node.get('id'),
                node.get('user_id'),
                True
            )
            self.communicate(
                self.configuration,
                f"{node.get('url', None)}?token={self.configuration.WEBHOOK_TOKEN}",
                {'status': True}
            )

    def shutdown(self, nodes=None):
        for node in nodes:
            self.communicate(
                self.configuration,
                node.get('url', None),
                {'status': False}
            )

            self.write_log(
                'WEBHOOK',
                node.get('url', None),
                self.name,
                self._off_event_type,
                node.get('id'),
                node.get('user_id'),
                True
            )

    def run(self, callback = lambda x: x):
        ...

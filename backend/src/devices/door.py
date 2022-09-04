from devices.HttpDevice import HttpDevice


class Door(HttpDevice):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, off_type='Lock', on_type='Unlock')

    def initialize(self, nodes=None):
        super().initialize(nodes)

    def shutdown(self, nodes=None):
        super().shutdown(nodes)

    def run(self, callback = lambda x: x):
        ...

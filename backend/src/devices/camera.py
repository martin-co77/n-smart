import cv2

from devices.device import Device


class Camera(Device):
    cap = None
    _cancel_loop = False
    device_url = 0

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        """
        super().__init__(self, *args, **kwargs)
        if kwargs is not None and 'device_url' in kwargs:
            self.device_url = kwargs['device_url']

    def initialize(self, nodes=None):
        """
        Initialize
        :return:
        """
        if self.cap is not None:
            return
        print(f"Initialized {self.name}")
        self.cap = cv2.VideoCapture(self.device_url)

    def _post_init(self):
        """
        Called after initialization/cleanup
        :return:
        """
        self._cancel_loop = False
        self.cap = None

    def shutdown(self, nodes=None):
        """
        Shutdown the frames
        :return:
        """
        self._cancel_loop = True

    def run(self, callback=lambda x: x):
        """
        Start running the frames
        :param callback:
        :return:
        """

        if self.cap is None:
            self.initialize([])

        while self.cap.isOpened():
            if self._cancel_loop:
                self._post_init()
                break

            _, self.data = self.cap.read()

            self.on_timer(self.data)
            callback(self.data)

    @property
    def width(self):
        """
        Video Width
        :return:
        """
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def height(self):
        """
        Video Height
        :return:
        """
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def fps(self):
        """
        Frames per seconds (FPS)
        :return:
        """
        return self.cap.get(cv2.CAP_PROP_FPS)




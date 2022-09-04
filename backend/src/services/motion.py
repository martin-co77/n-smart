import time
import cv2
from config import AppConfig
from devices.camera import Camera
from exception.device import DeviceException
from exception.invalid_class import InvalidClassException
from exception.not_found import NotFoundException
from services.alarm import Alarm
from services.service import Service
from services.daemon import Daemon


class MotionDetection(Service, Daemon):

    """
    Contains background subtraction algo with Gaussian mixture model
    """
    fgbg = None

    """
    Start time, used to subtract a time
    """
    _start_time = None

    f"""
    ::type {Camera}
    """
    device = None

    alarm: Alarm = None

    initializing: bool = False

    def __init__(self, *args, **kwargs):
        f"""
        This is responsible for detecting motion
        Gaussian Mixture model based background subtraction
        :param configuration:
        :param recorder:
        ::raise {DeviceException}
        """
        super().__init__(*args, **kwargs)

        if 'alarm' not in kwargs:
            raise NotFoundException('Service Alarm is required for motion detection')

        if not isinstance(kwargs['alarm'], Alarm):
            raise InvalidClassException(f"Alarm must be instance of Alarm, {type(kwargs['alarm'])} provided")

        self.alarm = kwargs['alarm']
        self.fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        self.device = self.devices.get_device(AppConfig.DEFAULT_DEVICE['MOTION_CAMERA'])

    def pin_time(self):
        """
        Pin the current time as start for further computation
        """
        self._start_time = time.time()

    @property
    def is_ready(self):
        """
        Verify if initialization phase has been passed and the algo
        is ready to start detecting motion, useful for Gaussian mixture algorithm
        """
        return time.time() - self._start_time > self.configuration.MOTION_INIT_SEC

    @staticmethod
    def detect_motion(frame):
        """
        Detect motion using the OpenCV contours bigger than 5000
        """
        cnts, hierarchies = cv2.findContours(frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        for cnt in cnts:
            cnt_area = cv2.contourArea(cnt)

            if cnt_area < 5000:
                continue
            else:
                return True

        return False

    def _process_frames(self, frames, config):
        """
        Called for any individual frames
        Start processing frames
        :param frames:
        :param config:
        :return:
        """
        self.device.initialize()

        frame = frames

        fgmask = self.fgbg.apply(frame, learningRate=0.001)
        can_print_status = config['index'] % 100 == 0
        if self._stop_video:
            self.device.shutdown()

        if not self.is_ready and not config['init_done']:
            if not self.initializing:
                self.initializing = True
                print(f"Initializing {(int (time.time() - self._start_time))} secs of {self.configuration.MOTION_INIT_SEC} secs. Please wait...") if can_print_status else ...
            return

        if self.initializing:
            self.initializing = False
            print(f" Initialization 60/60 complete!")

        config['init_done'] = True
        is_motion_detected = self.detect_motion(fgmask)

        if not is_motion_detected and self.recorder.is_active:
            if not config['stop_loop']:
                config['stop_loop'] = True
                self.pin_time()
            if config['stop_loop'] and time.time() - self._start_time > self.configuration.TILL_RECORD:
                self.recorder.clear()
                print("motion stopped ...")
            return
        elif is_motion_detected and self.recorder.is_active:

            self.recorder.record(frame)
            config['stop_loop'] = False

        elif is_motion_detected and not self.recorder.is_active:
            config['stop_loop'] = False
            print("Motion detected")
            self.recorder.setup(self.device.fps, self.device.width, self.device.height)
            try:
                if len(self.configuration.CURRENT_USER) < 1:
                    self.alarm.trigger(self.recorder.recording_url)
                self.configuration.event.call('motion', **{'frame': frame, 'device': self.device.name})
            except Exception as e:
                print("exception ", e.__str__())

    def start(self):
        """
        Start the detection
        Opens the camera and prepare the frame for detection
        :return:
        """
        self.pin_time()

        config = {
            'index': 0,
            'stop_loop': False,
            'init_done': False
        }
        self.device.on_timer = lambda x: self._process_frames(x, config)

    @property
    def _stop_video(self):
        """
        Monitors if the cancel key has been pressed to exit off the loop
        """
        k = cv2.waitKey(1) & 0xff
        if k == ord('q'):
            return True




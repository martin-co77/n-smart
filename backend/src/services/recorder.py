import os
from os.path import abspath
from flask import Flask, request
from config import AppConfig
import cv2


class Recorder:
    """
    Suffix to the recorded file for each motion
    """
    index: int = 0

    """
    Configuration
    """
    configuration: AppConfig = None

    """
    writer for recorder
    """
    writer = None

    """
    if recorder is currently recording
    """
    active: bool = False

    def __init__(self, configuration: AppConfig):
        self.configuration = configuration

    def setup(self, fps: float, width: int, height: int):
        """
        Initial setup for recorder
        :param height:
        :param width:
        :param fps:
        :return:
        """
        if self.writer is not None:
            self.writer.release()

        self.index += 1

        print(f"FPS {fps} \r\nWidth {width} \r\nHeight {height}")

        self.writer = cv2.VideoWriter(
            self.recording_file,
            self.configuration.FOURCC,
            fps,
            (
                width,
                height
            )
        )
        self.active = True

    def record(self, frame):
        """
        Write recording to file
        :param frame:
        :return:
        """
        self.writer.write(frame)

    @property
    def is_active(self):
        """
        Checks if recording is currently active
        :return:
        """
        return self.active

    def clear(self):
        """
        Clear, i.e prepare for new recording
        :return:
        """
        self.active = False

    @property
    def recording_file(self):
        return abspath(os.path.join(self.configuration.UPLOAD_DIR, f"{self.configuration.FILE_PREFIX}{self.index}.{self.configuration.EXTENSION}"))

    @property
    def recording_url(self):
        return f"{self.configuration.HOST_NAME}/{self.configuration.FILE_PREFIX}{self.index}.{self.configuration.EXTENSION}"

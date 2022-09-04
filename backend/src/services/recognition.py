import tempfile

import cv2
import os
from config import AppConfig
from devices.camera import Camera
from lib.request import Request
from services.service import Service


class Facials(Service):
    """
    Gallery being authorized against
    """
    gallery_name = "Authorized"



    """
    Headers file for the request
    """
    headers = dict()

    f"""
    ::type {Camera}
    """
    device = None

    """
    :type {str}
    """
    image_file: str = None

    """
    Initializer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = Request(self.configuration)
        self.request.clear_header()\
            .set_header('app_id', self.configuration.APP_ID)\
            .set_header('app_key', self.configuration.APP_KEY)
        self.device = self.devices.get_device(AppConfig.DEFAULT_DEVICE['DOOR_CAMERA'])
        self.image_file = self._get_create_temp_file()

    def post_recognizer(self, path: str, callback=lambda x: x):
        self.headers.update({
            'Content-Type': None
        })
        authorized = self.request.post(
            f"{self.configuration.API_DOMAIN}/recognize",
            {
                'gallery_name': self.gallery_name
            },
            {
                'image': (path, open(path, 'rb'))
            })
        subject_id = authorized['images'][0]['transaction'].get('subject_id') if 'images' in authorized else None
        callback((subject_id, authorized))
        return subject_id, authorized

    def recognize(self):
        """
        This provides the necessary functionality to authorize i.e recognize the
        user that has been previously enrolled via their name
        :return:
        """
        data = self.device.get_data()
        cv2.imwrite(self.image_file, data)
        return self.post_recognizer(self.image_file)

    def _post_add_user(self, name, path):
        """
        Enroll User face
        :param name:
        :param path:
        :return:
        """
        self.headers.update({
            'Content-Type': None
        })

        return self.request.post(f"{self.configuration.API_DOMAIN}/enroll", {
            'subject_id': name,
            'gallery_name': self.gallery_name
        }, {
            'image': (path,  open(path, 'rb')),
        })

    def add_user(self, name: str, path):
        """
        Enroll User face
        :param name:
        :param path:
        :return:
        """
        return self._post_add_user(name, path)

    def _get_create_temp_file(self):
        """
        Create and return the temp file for this instance
        :return:
        """
        return os.path.join(self.configuration.temp_directory, self.configuration.image_name_timer)

    def _process_frames(self, frame, callback=lambda x: x):
        """
        Process frames
        :param frame:
        :param config:
        :param callback:
        :return:
        """

        cv2.imwrite(self.image_file, frame)

        if callable(callback):
            callback(self.image_file)


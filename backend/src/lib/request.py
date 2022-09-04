import requests

from config import AppConfig


class Request:
    configuration: AppConfig = None
    header = None

    def __init__(self, config: AppConfig):
        f"""
        :param {AppConfig} config: 
        """
        self.configuration = config
        self.clear_header()

    def clear_header(self):
        self.headers = {}
        return self

    def set_header(self, key, value):
        """
        Set the header
        :param key:
        :param value:
        :return:
        """
        self.headers[key] = value
        return self

    """
    Provides request functionality
    """
    def send(self, url: str, method: str, data = None, files = None, json = None):
        """
        :param json:
        :param url:
        :param method:
        :param data:
        :param files:
        :return:
        """
        if method == 'head':
            send = requests.head(
                url = url,
                headers = self.headers
            )
        elif method == 'post':
            send = requests.post(
                url=url,
                files=files,
                data=data,
                json=json,
                headers=self.headers,
            )
        else:
            send = requests.get(
                url = url,
                headers = self.headers
            )
        return send.json()

    def post(self, path: str, data = None, files = None, json=None):
        """
        :param json:
        :param {str} path:
        :param data:
        :param files:
        :return:
        """
        return self.send(path, 'post', data, files, json)

    def get(self, path: str):
        """
        :param path:
        :return:
        """
        return self.send(path, 'get')

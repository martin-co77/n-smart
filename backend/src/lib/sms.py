from config import AppConfig
from lib.request import Request


class SMS:
    configuration: AppConfig = None
    _request = None

    def __init__(self, configuration: AppConfig):
        """
        :param configuration:
        """
        self.configuration = configuration
        self._request = Request(configuration)
        self._request.clear_header()\
            .set_header('Content-Type', 'application/json')\
            .set_header('Authorization', configuration.CHECKMOBIL_SECRET)

    def send(self, to: str, message: str):
        """
        :param to:
        :param message:
        :return:
        """
        response = self._request.post(f"{self.configuration.CHECKMBOBI_DOMAIN}/sms/send",json= {
            "from": self.configuration.PROJECT_NAME,
            "to": to,
            "text": message,
            "platform": "web"
        })

        return response

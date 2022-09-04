from config import AppConfig
import mailchimp_transactional


class Email:
    configuration: AppConfig = None
    mailchimp = None

    def __init__(self, configuration: AppConfig):
        """
        Sends E-mail
        :param configuration:
        """
        self.configuration = configuration
        self.mailchimp = mailchimp_transactional.Client(self.configuration.MAILCHIMP_KEY)

    def send(self, to: str, subject: str, message: str):
        """
        Sends transaction email using mailchimp
        :param to:
        :param subject:
        :param message:
        :return:
        """
        self.mailchimp.messages.send({
            'message': {
                'from_email': self.configuration.PROJECT_EMAIL,
                'subject': subject,
                'text': message,
                'to': [{'email': to, 'type': 'to'}]
            }

        })


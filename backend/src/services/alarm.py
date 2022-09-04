from config import AppConfig
from lib.email import Email
from lib.mysql import MySQL
from lib.sms import SMS
from system import System


class Alarm(System):

    f"""
    :type {SMS}
    """
    sms: SMS = None

    f"""
    :type {Email}
    """
    email: Email = None

    def __init__(
            self,
            configuration: AppConfig,
            db: MySQL
    ):
        super().__init__(configuration=configuration, db=db)
        """
        Alarm service
        :param configuration:
        :param db:
        """
        self.sms = SMS(self.configuration)
        self.email = Email(self.configuration)

    def trigger(self, recording_path: str):
        """
        Trigger
        :param recording_path:
        :return:
        """
        self.send_alarm(recording_path)

    def send_alarm(self, recording_path: str):
        """
        send the alarm
        :param recording_path:
        :return:
        """
        users = self.get_alarm_users()

        for user in users:
            alarm_msg = self._alarm_message(user.get('name'), recording_path)
            destination = None
            origin = None
            if user.get('phone') is not None:
                self.sms.send(user.get('phone'), alarm_msg)
                destination = user.get('phone')
                origin = 'Phone'

            if user.get('email') is not None:
                self.email.send(user.get('email'), 'Intruder Alarm', alarm_msg)
                destination = user.get('email')
                origin = 'Email'

            self.write_log(
                'INTRUSION',
                destination,
                origin,
                'Alarm',
                user.get('id'),
                user.get('id'),
                True
            )

    def _alarm_message(self, name, recording_link):
        """
        This provides the SQL query to fetch alarm users
        :return:
        """
        return f"Hello {name}\n " \
               f"Intruder has been detected on your premises. \n\r" \
               f"To view the intruder video, please click on this link {recording_link}"

    def get_alarm_users(self):
        """
        Aggregate all alarm users
        :return:
        """

        return self.db.set_query(
            f"SELECT a.email, a.phone, a.user, a.id, CONCAT(u.firstname, ' ', u.lastname) as name "
            f"FROM alarm a INNER JOIN `user` u on u.id=a.user "
            f"{'WHERE a.user IN %s' if len(self.configuration.CURRENT_USER) > 0  else ''}",
            (self.configuration.CURRENT_USER,) if len(self.configuration.CURRENT_USER) else ()
        )

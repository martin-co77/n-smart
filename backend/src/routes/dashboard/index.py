from lib.authorizer import Authorizer
from routes.controller import Controller
from services.response import Response


class Dashboard(Controller):

    @Authorizer.token_authorizer
    def index(self, current_user):
        tables = self.configuration.TABLES
        response = Response()
        stat = self.db.set_query(
            f"SELECT l.created_at, CONCAT(u.firstname, ' ' , u.lastname) as name,"
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} WHERE `type`=%s AND `status`=%s) as success_auth, "
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} WHERE `type`=%s AND `status`=%s) as failed_auth "
            f"FROM {tables.get('LOG')} l INNER JOIN {tables.get('USER')} u on u.id=l.user_associated WHERE l.type=%s "
            f"ORDER BY l.created_at DESC LIMIT 1",
            ('RECENT_LOGIN', 1, 'RECENT_LOGIN', 0, 'RECENT_LOGIN')
        )

        recent_logins = self.db.set_query(
            f"SELECT CONCAT(u.firstname, ' ', u.lastname) as name, destination, l.created_at, status FROM {tables.get('LOG')} l LEFT JOIN {tables.get('USER')} u on u.id=l.user_associated WHERE l.type=%s ORDER BY l.created_at DESC LIMIT 10",
            ('RECENT_LOGIN',)
        )

        speech_grammar = self.db.set_query(
            f"SELECT DISTINCT name FROM {tables.get('WEBHOOK')}",
            ()
        )

        recent_users = self.db.set_query(
            f"SELECT CONCAT(u.firstname, ' ', u.lastname) as name, u.last_login, u.picture, "
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} u1 WHERE u1.user_associated = l.user_associated AND u1.type=%s) as authorizations, "
            f"(SELECT COUNT(id) FROM {tables.get('LOG')} u1 WHERE u1.user_associated = l.user_associated AND u1.type=%s) as alerts "
            f" FROM {tables.get('LOG')} l INNER JOIN {tables.get('USER')} u on u.id = l.user_associated WHERE l.type=%s GROUP BY u.id ORDER BY u.id DESC LIMIT 10",
            ('RECENT_LOGIN', 'INTRUSION', 'RECENT_LOGIN')
        )

        recent_intruders = self.db.set_query(
            f"SELECT "
            f"  CONCAT(u.firstname, ' ', u.lastname) as name, l.created_at, l.destination "
            f"FROM {tables.get('LOG')} l INNER JOIN {tables.get('USER')} u on u.id = l.user_associated WHERE l.type=%s ORDER BY l.created_at DESC LIMIT 10",
            ('INTRUSION',)
        )

        recent_webhooks = self.db.set_query(
            f"SELECT "
            f"l.origin, l.created_at, l.destination, l.msg, l.status "
            f"FROM {tables.get('LOG')} l WHERE l.type=%s ORDER BY l.created_at DESC LIMIT 10",
            ('WEBHOOK',)
        )

        return response.set('success', True, 200, {
            'statistics': stat,
            'logins': recent_logins,
            'users': recent_users,
            'intruders': recent_intruders,
            'webhooks': recent_webhooks,
            'grammar': speech_grammar
        }).jsonify()

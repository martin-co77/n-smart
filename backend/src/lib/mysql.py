from config import AppConfig
from flask_mysqldb import MySQL as flash_mysql


class MySQL:
    db = None
    app = None
    _query = None
    _data = None

    def __init__(self, app, configuration: AppConfig):
        """
        :param app:
        :param configuration:
        """
        app.config['MYSQL_HOST'] = configuration.DB_CONFIG.get('host', None)
        app.config['MYSQL_USER'] = configuration.DB_CONFIG.get('user', None)
        app.config['MYSQL_PASSWORD'] = configuration.DB_CONFIG.get('password', None)
        app.config['MYSQL_CURSORCLASS'] = configuration.DB_CONFIG.get('cursor_class', None)
        app.config['MYSQL_DB'] = configuration.DB_CONFIG.get('db', None)
        self.app = app
        self.db = flash_mysql(self.app)

    def execute_sql(self):
        """
        Execute query
        :return:
        """
        with self.app.app_context():
            cursor = self.db.connection.cursor()
            cursor.execute(self._query, self._data)
            self.db.connection.commit()
            data = cursor.fetchall()
            cursor.close()
            return data

    def insert(self, table: str, values: dict):
        """
        Insert into database
        :param table:
        :param values:
        :return:
        """
        self._query = f"INSERT INTO `{table}` ({','.join(['`'+key+'`' for key in values])}) " \
                      f"VALUES ({','.join(['%s' for _, value in values.items()])})"
        self._data = tuple(values.get(key) for key in values)
        return self.execute_sql()

    def set_query(self, query, data):
        """
        Set a query to be executed
        :param query:
        :param data:
        :return:
        """
        self._query = query
        self._data = tuple(item for item in data)
        return self.execute_sql()

    def delete(self, table, key, value):
        """
        Delete by key
        :param table:
        :param key:
        :param value:
        :return:
        """
        self._query = f"DELETE FROM {table} WHERE `{key}` = %s"
        self._data = (value,)
        return self.execute_sql()

    def update(self, table, values: dict, key: str, value):
        """
        Update MySQL
        :param table:
        :param values:
        :param key:
        :param value:
        :return:
        """
        self._query = f"UPDATE `{table}` SET {','.join([ '`'+_+'`' + '=%s' for _ in values])} WHERE `{key}` = %s"
        self._data = tuple([*[values.get(key) for key in values], value])
        return self.execute_sql()



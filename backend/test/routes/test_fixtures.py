from unittest import TestCase, mock
from unittest.mock import MagicMock

from src.main import Main
main = Main()

init = False


class TestFixtures(TestCase):
    ctx = None
    client = None
    db = None
    set_query_return = list()
    set_delete_return = list()

    def build_db_test(self):
        db = MagicMock()
        db.insert = MagicMock(return_value=1)
        db.set_query = MagicMock(return_value= self.set_query_return)
        db.delete = MagicMock(return_value=self.set_delete_return)
        return db

    @classmethod
    def setUpClass(cls) -> None:
        cls.db = cls.build_db_test(cls)
        main.db = cls.db
        global init

        if not init:
            init = True
            with mock.patch('src.main.threading.Thread') as th:
                main.post_run()


        cls.ctx = main.app.app_context()
        cls.ctx.push()
        cls.client = main.app.test_client()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ctx.pop()

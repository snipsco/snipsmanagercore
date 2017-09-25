from unittest import TestCase

from snipsskillscore.server import Server


class TestServer(TestCase):

    def setUp(self):
        self.server = Server("localhost", 9898, False, [], None)

    def test_server(self):
        self.assertEqual(1, 1)

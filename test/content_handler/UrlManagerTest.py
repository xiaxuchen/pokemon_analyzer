import unittest
from content_handler.PythonSetUrlManager import PythonSetUrlManager

urlManager = None


class TestUrlManager(unittest.TestCase):

    def setUp(self):
        global urlManager
        urlManager = PythonSetUrlManager()

    def test_should_baidu_waiting(self):
        urlManager.add_url("http://www.baidu.com", "test")
        self.assertEqual(urlManager.pop_url()[0], "http://www.baidu.com")

    def test_should_tag_equal(self):
        urlManager.add_url("http://www.baidu.com", "plain")
        self.assertEqual(urlManager.pop_url()[1], "plain")

    def test_should_empty(self):
        urlManager.add_url("http://www.baidu.com", "test")
        urlManager.pop_url()
        urlManager.add_url("http://www.baidu.com", "test")
        self.assertEqual(None, urlManager.pop_url())
import unittest
from content_handler.UrlHandler import UrlHandler
from exception import IllegalArgumentException


class UrlHandlerTest(unittest.TestCase):

    def test_should_get_absolute_path(self):
        handler = UrlHandler()
        self.assertEqual(handler.handle_url("http://www.baidu.com", "/load?name=xxc"),
                         "http://www.baidu.com/load?name=xxc")
        self.assertEqual(handler.handle_url("http://www.baidu.com?q=111", "/load?name=xxc"),
                         "http://www.baidu.com/load?name=xxc")
        self.assertEqual(handler.handle_url("http://www.baidu.com?q=111#comment", "/load?name=xxc"),
                         "http://www.baidu.com/load?name=xxc")
        self.assertEqual(handler.handle_url("http://www.baidu.com/name/age", "../load?name=xxc"),
                         "http://www.baidu.com/name/load?name=xxc")
        self.assertEqual(handler.handle_url("http://www.baidu.com/name/age", "../../load?name=xxc"),
                         "http://www.baidu.com/load?name=xxc")

        self.assertEqual(handler.handle_url("http://www.baidu.com/name/age",
                                            "http://www.baidu.com/load?name=xxc"),
                         "http://www.baidu.com/load?name=xxc")
        self.assertEqual(handler.handle_url("http://www.baidu.com/name/age",
                                            "https://www.baidu.com/load?name=xxc"),
                         "https://www.baidu.com/load?name=xxc")
        self.assertRaises(IllegalArgumentException, lambda: handler.handle_url(None, None))
        self.assertRaises(IllegalArgumentException, lambda: handler.handle_url(None, "/load.html"))
        self.assertRaises(IllegalArgumentException, lambda: handler.handle_url(None, "http://www.baidu.com"))
        self.assertEqual(handler.handle_url("http://www.baidu.com", None), None)


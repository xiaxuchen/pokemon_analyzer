from content_handler.UrlManager import UrlManager
from threading import RLock


class PythonSetUrlManager(UrlManager):

    def __init__(self, exclude=set()):
        self.wait_dict = dict()
        self.old_set = set()
        self.exclude = exclude
        # 锁
        self.lock = RLock()

    def add_url(self, url, tag):
        if tag in self.exclude:
            return
        self.lock.acquire(blocking=True)
        try:
            if url not in self.old_set:
                self.wait_dict[url] = tag
        finally:
            self.lock.release()

    def pop_url(self):
        self.lock.acquire(blocking=True)
        try:
            if len(self.wait_dict) > 0:
                url, tag = self.wait_dict.popitem()
                self.old_set.add(url)
                return url, tag
            else:
                return None
        finally:
            self.lock.release()

    def has_next(self):
        return len(self.wait_dict) > 0


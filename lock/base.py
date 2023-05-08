import abc


class Lock(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def lock(self):
        pass

    def unlock(self):
        pass

__author__ = 'hasier'

from threading import Thread


def async(f):
    """Makes the decorated method asynchronous"""
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper
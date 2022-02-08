import threading

class Workers():

    # threads = []
    cv = threading.Condition()
    done = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Workers, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
        return cls.instance

if __name__ == "__main__":

    w = Workers()

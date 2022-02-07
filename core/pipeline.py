class Pipeline():

    queue = []
    show_idx = 0
    save_idx = 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Pipeline, cls, *args, **kwargs).__new__(cls, *args, **kwargs)
        return cls.instance

    def push(self, palette):
        self.queue.append(palette)

    def pop(self):
        self.queue.pop(0)

if __name__ == "__main__":
    p = Pipeline()
    p.push(1)
    p1 = Pipeline()
    p1.push(2)

import threading
import cv2

from core.pipeline import Pipeline
from core.palette import Palette
from core.plasma import PlasmaModule

cv = threading.Condition()
threads = []
idx = 0
done = False

class Consumer(threading.Thread):

    pipeline = Pipeline()

    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        # shor_result
        while done == False:
            global cv
            cv.acquire()
            while len(self.pipeline.queue) <= self.pipeline.show_idx:
                print('consumer({}) waiting...'.format(self.id))
                cv.wait()
            print(type(self.pipeline.queue[self.pipeline.show_idx]))
            print('consumer({}) popping...'.format(self.id))
            print(self.pipeline.queue[self.pipeline.show_idx])
            img_new = self.pipeline.queue[self.pipeline.show_idx]
            self.pipeline.show_idx += 1
            cv.release()

class Producer(threading.Thread):

    pipeline = Pipeline()
    palette = Palette(fabric=2000, path='/')

    def __init__(self, id, rpm, conveyor_speed_m):
        threading.Thread.__init__(self)
        self.id = id
        self.rpm = rpm
        self.conveyor_speed_m = conveyor_speed_m

    def run(self):
        global cv

        # rpm = 120
        # conveyor_speed_m = 1000

        if (self.rpm != None and self.conveyor_speed_m != None):
            center = [int(self.palette._FABRIC / 2), int(self.palette._FABRIC / 2)]
            self.palette.set_plasma(PlasmaModule(center=center, nPlasma=self.palette._nPlasma, R=self.palette._R, r=self.palette._r, zoom=self.palette._ZOOM),
                            rpm=self.rpm, conveyor_speed_m=self.conveyor_speed_m)
            self.palette.draw_plasma()
            self.palette.generate_palette_image(imshow=False)

            for t in range(0, 10):
                split = 1024 * 2  # rpm에 반비례하게 값을 정해줘야할듯

                for i in range(1, split):
                    self.palette.draw_plasma(split=split)
                    if (i % 10 == 0):
                        print('producing({}) image...'.format(self.id))
                        self.palette.generate_palette_image(save=False, imshow=False)
                        cv.acquire()
                        self.palette.pipeline.push(self.palette._PALETTE.copy())
                        cv.notify()
                        cv.release()

            done = True

class Workers():

    threads = []

    def add_consumer(self):
        th = Consumer(1)
        threads.append(th)
        th.start()
        th.join()

    def add_producer(self):
        th = Producer(1)
        threads.append(th)
        th.start()
        th.join()

    def run(self, rpm, conveyor_speed_m):
        threads.append(Producer(1, rpm, conveyor_speed_m))
        threads.append(Consumer(1))

        for th in threads: th.start()
        for th in threads: th.join()

        print('<END>')

if __name__ == "__main__":

    rpm = 120
    conveyor_speed_m = 1000

    w = Workers()
    w.run(rpm, conveyor_speed_m)

from threading import Thread
from PIL import Image
import os


class ImageResizer:
    def __init__(self, queue, from_directory, to_directory):
        self._queue = queue
        self._from_directory = from_directory
        self._to_directory = to_directory

    def resize(self, width, height, workers):
        for i in range(workers):
            t = Thread(target=self._resize_next_image, args=(width, height))
            t.daemon = True
            t.start()

        self._queue.join()

    def _resize_next_image(self, width, height):
        while True:
            image_name = self._queue.get()
            print 'resizing image ' + image_name + ' to ' + str(width) + 'x' + str(height)
            image = Image.open(self._from_directory + os.sep + image_name)
            image = image.resize((width, height), Image.ANTIALIAS)
            image.save(self._to_directory + os.sep + image_name, quality=100)
            self._queue.task_done()
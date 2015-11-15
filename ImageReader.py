import re
import os
from ImageResizer import ImageResizer
import Queue


class ImageReader:
    def __init__(self, image_directory):
        self._image_directory = image_directory

    def get_image_list(self):
        images = os.listdir(self._image_directory)
        images = self._order_images_by_name(images)
        images_paths = {}
        i = 0

        for index in images:
            images_paths[i] = images[index]
            i += 1

        return images_paths

    def resize_images(self, width, height, location, workers):
        images = self.get_image_list()
        queue = Queue.Queue()
        from_directory = self._image_directory
        to_directory = location

        for index in images:
            queue.put(images[index])

        image_resizer = ImageResizer(queue, from_directory, to_directory)
        image_resizer.resize(width, height, workers)

    def _order_images_by_name(self, images):
        tmp_images = {}
        for image in images:
            index = self._get_image_index_by_name(image)
            tmp_images[index] = image

        return tmp_images

    @staticmethod
    def _get_image_index_by_name(image):
        index = -1

        for match in re.finditer('[0-9]*', image):
            match_string = match.group(0)
            if match_string:
                index = int("%10d" % int(match_string))
                break  # use first match (i.e. for images like Image(2-4))

        return index

# ffmpeg -framerate 1 -pattern_type glob -i '*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
# https://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images

import os
import shutil
import tempfile
from PIL import Image


class Renderer:
    def __init__(self, signals_reader, image_reader, audio_file, output_file_name):
        self._signalsReader = signals_reader
        self._imageReader = image_reader
        self._audioFile = audio_file
        self._outputFileName = output_file_name

    def render(self, width, height, workers):
        self._create_tmp_dir()
        self._create_offset_image(width, height)

        self._imageReader.resize_images(width, height, self._tmp_image_dir, workers)
        images = self._imageReader.get_image_list()
        signals = self._signalsReader.get_rows()

        for index in images:
            image_path = self._tmp_image_dir + os.sep + images[index]
            duration = int(signals[index]['duration'])
            start = int(signals[index]['second'])
            self._create_link(image_path, start, duration)

        self._render_video()
        self._remove_tmp_dir()

    def _create_offset_image(self, width, height):
        signals = self._signalsReader.get_rows()
        start = signals[0]['second']

        if start > 0:
            duration = start
            new_image = Image.new('RGB', (width, height), "black")
            image_path = self._tmp_image_dir + os.sep + 'offset.jpg'
            new_image.save(image_path)
            self._create_link(image_path, 0, int(duration))

    def _render_video(self):
        command = "ffmpeg -framerate 1 -pattern_type glob -i '"
        command += self._tmpLinkDir + os.sep + "*.jpg' -i " + self._audioFile
        command += " -c:v libx264 -c:a aac -strict -2 -r 30 -pix_fmt yuv420p "
        command += self._outputFileName + ".mp4"

        os.system(command)

    def _create_link(self, image_path, start, duration):
        for i in range(0, duration):
            output_file_name = '{0:010d}'.format((start + i))
            link_name = self._tmpLinkDir + os.sep + output_file_name + '.jpg'
            os.symlink(image_path, link_name)

    def _create_tmp_dir(self):
        self._tmpDir = tempfile.mkdtemp()
        self._tmp_image_dir = self._tmpDir + os.sep + 'images'
        self._tmpLinkDir = self._tmpDir + os.sep + 'links'
        os.mkdir(self._tmp_image_dir)
        os.mkdir(self._tmpLinkDir)

    def _remove_tmp_dir(self):
        shutil.rmtree(self._tmpDir)

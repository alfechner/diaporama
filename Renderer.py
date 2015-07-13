#ffmpeg -framerate 1 -pattern_type glob -i '*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
#https://trac.ffmpeg.org/wiki/Create%20a%20video%20slideshow%20from%20images

import os
import shutil
import tempfile
import PIL
from PIL import Image

class Renderer:
	def __init__(self, signalsReader, imageReader, audioFile, outputFileName):
		self._signalsReader = signalsReader 
		self._imageReader = imageReader
		self._audioFile = audioFile
		self._outputFileName = outputFileName

	def render(self, width, height):
		self._createTmpDir()
		self._createOffsetImage(width, height)

		self._imageReader.resizeImages(width, height, self._tmpImageDir)
		images = self._imageReader.getImageList()
		signals = self._signalsReader.getRows()

		for index in images:
			imagePath = self._tmpImageDir + os.sep + images[index]
			duration = int(signals[index]['duration'])
			start = int(signals[index]['second'])
			self._createLink(imagePath, start, duration)
		
		self._renderVideo()
		self._removeTmpDir()
		
	def _createOffsetImage(self, width, height):
		signals = self._signalsReader.getRows()
		start = signals[0]['second']
		
		if start > 0:
			duration = start
			newImage = Image.new('RGB', (width, height), "black")
			imagePath = self._tmpImageDir + os.sep + 'offset.jpg'
			newImage.save(imagePath)
			self._createLink(imagePath, 0, int(duration))

	def _renderVideo(self):
		os.system("ffmpeg -framerate 1 -pattern_type glob -i '" + self._tmpLinkDir + os.sep + "*.jpg' -i " + self._audioFile + " -c:v libx264 -c:a aac -strict -2 -r 30 -pix_fmt yuv420p " + self._outputFileName + ".mp4")

	def _createLink(self, imagePath, start, duration):
		for i in range(0, duration):
			outputFileName = '{0:010d}'.format((start + i))
			linkName = self._tmpLinkDir + os.sep + outputFileName + '.jpg'
			os.symlink(imagePath, linkName)

	def _createTmpDir(self):
		self._tmpDir = tempfile.mkdtemp()
		self._tmpImageDir = self._tmpDir + os.sep + 'images'
		self._tmpLinkDir = self._tmpDir + os.sep + 'links'
		os.mkdir(self._tmpImageDir)
		os.mkdir(self._tmpLinkDir)

	def _removeTmpDir(self):
		shutil.rmtree(self._tmpDir)
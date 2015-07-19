import re
import os
import PIL
from PIL import Image

class ImageReader:
	def __init__(self, imageDir):
		self._imageDir = imageDir 

	def getImageList(self):
		images = os.listdir(self._imageDir)
		images = self._orderImagesByName(images)
		imagesPaths = {}
		i = 0

		for index in images:
			imagesPaths[i] = images[index]
			i = i + 1

		return imagesPaths

	def resizeImages(self, width, height, location):
		images = self.getImageList();
		for index in images:
			imageName = images[index]
			print 'resizie image ' + imageName + ' to ' + str(width) + 'x' + str(height)
			image = Image.open(self._imageDir + os.sep + imageName)
			image = image.resize((width, height), Image.ANTIALIAS)
			image.save(location + os.sep + imageName, quality=100)

	def _orderImagesByName(self, images):
		tmpImages = {}
		for image in images:
			index = self._getImageIndexByName(image);
			tmpImages[index] = image

		return tmpImages

	def _getImageIndexByName(self, image):
		for match in re.finditer('[0-9]*', image):
			matchString = match.group(0)
			if matchString: 
				index = int("%10d" % int(matchString))
				break # use first match (i.e. for images like Image(2-4))

		return index



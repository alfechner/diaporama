class SlideGenerator:
	def __init__(self, signalsReader, imageReader):
		self._signalsReader = signalsReader 
		self._imageReader = imageReader

	def getSlides(self, width, height):
		return self._filePath;
import os
from CsvReader import CsvReader
from ImageReader import ImageReader
from Renderer import Renderer
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="output filename (without extension)", metavar="FILE")
parser.add_option("-x", "--width", dest="width", default="300", help="output video width")
parser.add_option("-y", "--height", dest="height", default="200", help="output video height")

(options, args) = parser.parse_args()
print options
print args
try:

	if len(args) < 1:
		raise StandardError('no project directory specifed')

	project = args[0]

	if not os.path.isdir(project):
		raise StandardError('project directory could not be found')

	if options.filename is None:
		options.filename = project

	# init locations
	projectDir = project
	signalsFile = projectDir + os.sep + 'signals.csv'
	audioFile = projectDir + os.sep + projectDir + '.flac'
	imageDir = projectDir + os.sep + 'images'
	outputFileName = options.filename

	# init video properties
	width = int(options.width)
	height = int(options.height)

	signalsReader = CsvReader(signalsFile)
	imageReader = ImageReader(imageDir)
	renderer = Renderer(signalsReader, imageReader, audioFile, outputFileName)

	renderer.render(width, height)

except StandardError:
	parser.print_help()
	raise
	exit(-1)
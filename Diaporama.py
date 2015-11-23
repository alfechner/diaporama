import os
from CsvReader import CsvReader
from ImageReader import ImageReader
from Renderer import Renderer
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="output filename (without extension)", metavar="FILE")
parser.add_option("-a", "--audio-file", dest="audio_filename", help="audio file", metavar="FILE")
parser.add_option("-x", "--width", dest="width", default="300", help="output video width")
parser.add_option("-y", "--height", dest="height", default="200", help="output video height")
parser.add_option("-w", "--workers", dest="workers", default=8, help="number of workers for resizing images")


(options, args) = parser.parse_args()
print options
print args
try:

    if len(args) < 1:
        raise StandardError('no project directory specified.')

    project = args[0]

    if not os.path.isdir(project):
        raise StandardError('project directory could not be found.')

    audio_file = options.audio_filename

    if not os.path.isfile(audio_file):
        raise StandardError('audio file could not be found.')

    workers = options.workers
    workers = int(workers)

    if not type(workers) == int:
        raise StandardError('no valid amount of workers set.')

    if options.filename is None:
        options.filename = project

    # init locations
    project_dir = project
    signals_file = project_dir + os.sep + 'signals.csv'
    image_dir = project_dir + os.sep + 'images'
    output_file_name = options.filename

    # init video properties
    width = int(options.width)
    height = int(options.height)

    signals_reader = CsvReader(signals_file)
    image_reader = ImageReader(image_dir)
    renderer = Renderer(signals_reader, image_reader, audio_file, output_file_name)

    renderer.render(width, height, workers)

except StandardError:
    parser.print_help()
    raise

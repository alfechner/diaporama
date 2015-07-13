import csv

class CsvReader:
	def __init__(self, filePath):
		self._filePath = filePath

	def getRows(self):
		with open(self._filePath) as csvfile:
			reader = csv.DictReader(csvfile)

			rows = {}
			i = 0

			for row in reader:
				rows[i] = row
				i = i + 1

		return rows
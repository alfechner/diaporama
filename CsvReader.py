import csv


class CsvReader:
    def __init__(self, file_path):
        self._file_path = file_path

    def get_rows(self):
        with open(self._file_path) as csv_file:
            reader = csv.DictReader(csv_file)

            rows = {}
            i = 0

            for row in reader:
                rows[i] = row
                i += 1

        return rows

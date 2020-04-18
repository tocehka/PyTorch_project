import csv

class WriterManager:
    def __init__(self, file_name, header=False):
        self.file = open(file_name, 'w')
        if not header:
            self.writer = csv.writer(self.file)
        else:
            self.writer = csv.DictWriter(self.file, header)
            self.writer.writeheader()    
    def write_row(self, row):
        self.writer.writerow(row)
    def __del__(self):
        self.file.close()
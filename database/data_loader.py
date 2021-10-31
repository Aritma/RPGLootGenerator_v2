from pathlib import Path
from database.db_worker import DBWorker
import csv
# TODO: Replace prints with logger
import logging
import time


class CSVDataLoader:

    def __init__(self, source_dir: Path, db_worker: DBWorker):
        self.csv_list = self.get_csv_list(source_dir)
        self.db_worker = db_worker

    @staticmethod
    def get_csv_list(source_dir):
        return [csv_file for csv_file in source_dir.rglob("*.csv")]

    def load_file(self, file: Path):
        print(f"Loading: {file.name}")
        tic = time.perf_counter()
        with file.open(mode='r') as csv_file:
            rows = csv.reader(csv_file)
            for row in rows:
                name, description, *tags = row
                self.db_worker.register_item(
                    name=name, description=description, source=file.name, tags=tags
                )
        toc = time.perf_counter()
        print(f"Finished in {toc - tic:0.5f} seconds.")

    def load_all_files(self):
        for file in self.csv_list:
            self.load_file(file)

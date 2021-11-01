from gui.appgui import AppGUI
from pathlib import Path

from database.db_worker import DBWorker
from database.data_loader import CSVDataLoader

db_worker = DBWorker()

data_loader = CSVDataLoader(source_dir=Path.cwd().joinpath('data'), db_worker=db_worker)
data_loader.load_all_files()

db_worker.debug()  # Debug print of database tables

db_worker.engine.dispose()

app = AppGUI().run()

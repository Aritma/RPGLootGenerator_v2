from gui.appgui import AppGUI
from pprint import pprint
from pathlib import Path

from database.db_worker import DBWorker
from database.data_loader import CSVDataLoader

db_worker = DBWorker()

data_loader = CSVDataLoader(source_dir=Path.cwd().joinpath('data'), db_worker=db_worker)
data_loader.load_all_files()

db_worker.debug()  # Debug print of database tables

items1 = db_worker.get_items_with_tags(['fruit'])
pprint(items1)

items2 = db_worker.get_items_with_tags_combined(['common', 'fruit'])
pprint(items2)

db_worker.engine.dispose()

app = AppGUI().run()

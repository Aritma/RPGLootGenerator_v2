from typing import List
from sqlalchemy import create_engine, func, literal_column
from sqlalchemy.orm import Session
from database.db_tables import Base as DBTables_Base, ItemsTable, TagsTable
from structs.item import Item


class DBWorker:
    """DB Worker with SQL Alchemy declarative approach"""

    def __init__(self):
        self.engine = create_engine("sqlite:///:memory:")
        self.session = Session(self.engine)
        DBTables_Base.metadata.create_all(self.engine)

    def register_item(self, name: str, source: str, description: str, tags: List[str]) -> None:
        """Registers new item into the database."""
        item = ItemsTable(name=name, source=source, description=description)
        self.session.add(item)
        self.session.flush()  # Flush to assign item_id from autoincrement
        for tag in tags:
            tag = TagsTable(item_id=item.item_id, tag=tag)
            self.session.add(tag)
        self.session.flush()

    def get_items(self, item_ids: List) -> List[Item]:
        """Returns all items with item_ids from the list."""
        return [
            Item(
                item_id=item.item_id,
                name=item.name,
                source=item.source,
                description=item.description,
                tags=[tag for tag, in self.session.query(TagsTable.tag).filter(TagsTable.item_id == item.item_id)]
            ) for item in self.session.query(ItemsTable).filter(ItemsTable.item_id.in_(item_ids))
        ]

    def get_items_with_tags(self, tags: List[str]) -> List[Item]:
        """Returns all items which have at least one of tags from the list."""
        return self.get_items(
            [item.item_id for item in
             self.session.query(TagsTable.item_id)
                 .filter(TagsTable.tag.in_(tags))
                 .distinct()
             ]
        )

    def get_items_with_tags_combined(self, tags: List[str]) -> List[Item]:
        """Returns all items which have all the tags from the list."""
        return self.get_items(
            [item.item_id for item in
             self.session.query(TagsTable.item_id, func.count(TagsTable.item_id).label('c'))
                 .filter(TagsTable.tag.in_(tags))
                 .group_by(TagsTable.item_id)
                 .having(literal_column('c') >= len(tags))
             ]
        )

    def debug(self):  # <<<< DEBUG METHOD, WILL BE REMOVED LATER
        print("--------DEBUG--------")
        print([x for x in self.engine.execute("SELECT * FROM items")])
        print([x for x in self.engine.execute("SELECT * FROM tags")])
        print("------DEBUG_END------")

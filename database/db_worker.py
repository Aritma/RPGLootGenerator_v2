from typing import List
from sqlalchemy import create_engine, func, literal_column
from sqlalchemy.orm import Session, Query
from pprint import pprint

from database.db_tables import Base as DBTables_Base, ItemsTable, TagsTable
from structs.item import Item


class ItemBuilder:

    def __init__(self):
        self._query = Query(ItemsTable, TagsTable).join(TagsTable)

    @property
    def query(self):
        return self._query

    @query.getter
    def query(self):
        return self._query.distinct()

    def with_item_ids(self, item_ids: List[int]):
        self._query = self._query.filter(ItemsTable.item_id.in_(item_ids))
        return self

    def with_tags(self, tags: List[str]):
        self._query = self._query.filter(TagsTable.tag.in_(tags))
        return self

    # TODO: NOT WORKING -> Find the way to filter combined tags without creating new subquery
    # def with_tags_combined(self, tags: List[str]):
    #     self._query = self._query(TagsTable.item_id, func.count(TagsTable.item_id).label('c'))\
    #                    .filter(TagsTable.tag.in_(tags))\
    #                    .group_by(TagsTable.item_id)\
    #                    .having(literal_column('c') >= len(tags))

    def exclude_tags(self, tags: List[str]):
        self._query = self._query.filter(TagsTable.tag.not_in(tags))
        return self

    def exclude_item_ids(self, item_ids: List[int]):
        self._query = self._query.filter(ItemsTable.item_id.not_in(item_ids))
        return self


class DBWorker:

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

    def get_items(self, item_builder: ItemBuilder) -> List[Item]:
        return [
            Item(
                item_id=item.item_id,
                name=item.name,
                source=item.source,
                description=item.description,
                tags=[tag for tag, in self.session.query(TagsTable.tag).filter(TagsTable.item_id == item.item_id)]
            ) for item, in self.session.execute(item_builder.query)]

    def debug(self):  # <<<< DEBUG METHOD, WILL BE REMOVED LATER
        print("--------DEBUG--------")
        print([x for x in self.engine.execute("SELECT * FROM items")])
        print([x for x in self.engine.execute("SELECT * FROM tags")])
        pprint([x for x in self.get_items(ItemBuilder()
                                          .with_tags(tags=['common', 'meat'])
                                          .with_item_ids(item_ids=[1, 7, 8, 9])
                                          .exclude_item_ids([7, 9])
                                          )])
        print("------DEBUG_END------")

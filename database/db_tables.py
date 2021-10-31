from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ItemsTable(Base):
    __tablename__ = 'items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    source = Column(String)
    description = Column(String)


class TagsTable(Base):
    __tablename__ = 'tags'
    item_id = Column(Integer, ForeignKey('items.item_id'), primary_key=True)
    tag = Column(String, primary_key=True)

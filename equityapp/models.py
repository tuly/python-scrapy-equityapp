#! -*- coding: utf-8 -*-
import uuid
import json
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.dialects.postgresql import JSON
import settings

DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance.
    """
    return create_engine(URL(**settings.DATABASE))


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class EquityApartments(DeclarativeBase):
    """Sqlalchemy deals model"""
    __tablename__ = "listingsTable"

    id = Column(Integer, primary_key=True)
    listingData = Column(JSON)

    def __init__(self, item):
        item['_id'] = str(uuid.uuid4())
        self.listingData = json.dumps(dict(item))

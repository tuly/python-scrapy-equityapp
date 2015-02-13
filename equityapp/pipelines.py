# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import EquityApartments, db_connect, create_deals_table

class EquityappPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_deals_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.
        This method is called for every item pipeline component.
        """
        session = self.Session()

        # print item
        equity = EquityApartments(item)

        try:
            session.add(equity)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item

# -*- coding: utf-8 -*-

# Scrapy settings for equityapp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
BOT_NAME = 'equityapp'

SPIDER_MODULES = ['equityapp.spiders']
NEWSPIDER_MODULE = 'equityapp.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'equityapp (+http://www.yourdomain.com)'

ITEM_PIPELINES = ['equityapp.pipelines.EquityappPipeline']

DATABASE = {'drivername': 'postgres',
            'host': 'localhost',    # fill in your hostname here
            'port': '5432',
            'username': 'postgres', # fill in your username here
            'password': 'postgres', # fill in your password here
            'database': 'listingsDB'}
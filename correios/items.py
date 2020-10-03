# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CorreiosItem(scrapy.Item):
    localidade = scrapy.Field()
    faixa_de_cep = scrapy.Field()

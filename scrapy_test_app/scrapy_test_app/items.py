import scrapy

class Product(scrapy.Item):
  id = scrapy.Field()
  name = scrapy.Field()
  price = scrapy.Field()
  address = scrapy.Field()
  quantity = scrapy.Field()
  postage_type = scrapy.Field()
  url = scrapy.Field()

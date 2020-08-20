# -*- coding: utf-8 -*-
import scrapy
from scrapy_test_app.items import Product

class ScrapyProductSpiderSpider(scrapy.Spider):
  name = 'scrapy_product_spider'
  allowed_domains = ['poke-m.com']
  start_urls = ['https://poke-m.com/products?category=魚介類&area=tohoku']

  def parse(self, response):
    """
    レスポンスに対するパース処理
    """
    for product in response.css('.product-list .product-list__inner .product-panel--list-item'):
      yield Product(
        id = product.css('div::attr(data-id)').extract_first().strip(),
        name = product.css('div::attr(data-name)').extract_first().strip(),
        price = product.css('div::attr(data-price)').extract_first().strip(),
        address = product.css('p.product-box__address.icon-area-pin::text').extract_first().strip(),
        quantity = product.css('p.product-box__quantity::text').extract_first().strip(),
        postage_type = 1 if product.css('p.product-box__type.product-box__type--auto_coupon') else 0,
        url = response.urljoin(product.css('div.product-box a::attr(href)').extract_first().strip()),
      )

    # 再帰的にページングを辿るための処理
    older_product_link = response.css('div.pager a.icon-link__arrow.next::attr(href)').extract_first()
    if older_product_link is None:
      # リンクが取得できなかった場合は最後のページなので処理を終了
      return

    # URLが相対パスだった場合に絶対パスに変換する
    older_product_link = response.urljoin(older_product_link)
    print('*****************************************************')
    print(older_product_link)
    print('*****************************************************')
    # 次のページをリクエストを実行する
    yield scrapy.Request(older_product_link, callback=self.parse)
# from scrapy.contrib.spiders import CrawlSpider
# from scrapy.selector import Selector
# from scrapy.http import Request


# class YourCrawler(CrawlSpider):
#     name = "spider_name"
#     start_urls = [
#         'https://example.com/listviews/titles.php',
#     ]
#     allowed_domains = ["example.com"]

#     def parse(self, response):
#         # go to the urls in the list
#         s = Selector(response)
#         page_list_urls = s.xpath(
#             '///*[@id="tab7"]/article/header/h2/a/@href').extract()
#         for url in page_list_urls:
#             yield Request(response.urljoin(url), callback=self.parse_following_urls, dont_filter=True)

#         # Return back and go to bext page in div#paginat ul li.next a::attr(href) and begin again
#         next_page = response.css(
#             'ul.pagin li.presente ~ li a::attr(href)').extract_first()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield Request(next_page, callback=self.parse)

#     # For the urls in the list, go inside, and in div#main, take the div.ficha > div.caracteristicas > ul > li
#     def parse_following_urls(self, response):
#         # Parsing rules go here
#         for each_book in response.css('main#main'):
#             yield {
#                 'editor': each_book.css('header.datos1 > ul > li > h5 > a::text').extract(),
#             }

import scrapy


class CountrySpider(scrapy.Spider):
    name = 'countrySpider'
    allowed_domains = ['https://www.betexplorer.com']
    start_urls = [
        'https://www.betexplorer.com/soccer/',
    ]

    def parse(self, response):
        country_list = []
        name_list = []
        url_list = []
        name_list = response.css(
            '#countries-select .list-events__item__title *::text').getall()
        url_list = response.css(
            '#countries-select .list-events__item__title *::attr(href)').getall()
        for i in range(0, len(name_list)):
            country_list.append((name_list[i], url_list[i]))
        print(country_list)

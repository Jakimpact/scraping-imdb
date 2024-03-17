import scrapy


class ShowspiderSpider(scrapy.Spider):
    name = "showspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/toptv/"]

    def parse(self, response):
        pass

    def parse_show_page(self, response):
        pass

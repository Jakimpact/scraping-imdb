import scrapy


class ShowspiderSpider(scrapy.Spider):
    name = "showspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/"]

    def parse(self, response):
        pass

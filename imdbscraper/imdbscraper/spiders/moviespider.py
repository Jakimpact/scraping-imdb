import scrapy
from imdbscraper.items import MovieItem

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def parse(self, response):
        movies = response.xpath("//main//div[@data-testid='chart-layout-main-column']//ul[1]/li")

        for movie in movies:
            relative_url = movie.xpath("//a[last()]/@href").get()
            movie_url = "https://www.imbd.com/" + relative_url
            yield scrapy.Request(movie_url, callback=self.parse_movie_page)

    def parse_movie_page(self, response):
        
        movie_item = MovieItem()
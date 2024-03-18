import scrapy
from imdbscraper.items import MovieItem

class MoviespiderSpider(scrapy.Spider):
    name = "moviespider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    custom_settings = {
        'FEEDS': {
            'data/%(name)s/%(name)s_%(time)s.csv': {
                'format': 'csv',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        movies = response.xpath("//main//div[@data-testid='chart-layout-main-column']//ul[1]/li")

        for movie in movies:
            relative_url = movie.xpath(".//a[last()]/@href").get()
            if relative_url:
                movie_url = "https://www.imdb.com/" + relative_url
                yield scrapy.Request(movie_url, callback=self.parse_movie_page)

    def parse_movie_page(self, response):
        
        content = response.xpath("//main")
        movie_item = MovieItem()

        movie_item["url"] = response.url
        movie_item["title"] = content.xpath(".//h1/span[@data-testid='hero__primary-text']/text()").get()
        movie_item["original_title"] = content.xpath(".//h1/following-sibling::div/text()").get()
        movie_item["year"] = content.xpath(".//h1/following-sibling::ul/li[1]//text()").get()
        movie_item["public"] = content.xpath(".//h1/following-sibling::ul/li[2]//text()").get()
        movie_item["length"] = content.xpath(".//h1/following-sibling::ul/li[3]//text()").get()
        movie_item["imdb_rating"] = content.xpath(".//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[1]/text()").get()
        movie_item["num_imdb_raters"] = content.xpath(".//div[@data-testid='hero-rating-bar__aggregate-rating__score']/following-sibling::div/text()").get()
        movie_item["themes"] = content.xpath(".//div[@data-testid='genres']//text()").get()
        movie_item["synopsis"] = content.xpath(".//p[@data-testid='plot']//text()").get()
        movie_item["directors"] = content.xpath(".//p[@data-testid='plot']/following-sibling::div//li[@data-testid='title-pc-principal-credit'][1]//li//text()").getall()
        movie_item["writers"] = content.xpath(".//p[@data-testid='plot']/following-sibling::div//li[@data-testid='title-pc-principal-credit'][2]//li//text()").getall()
        movie_item["stars"] = content.xpath(".//p[@data-testid='plot']/following-sibling::div//li[@data-testid='title-pc-principal-credit'][3]//li//text()").getall()
        movie_item["metascore_rating"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[last()]//span[@class='score']//text()").get()
        movie_item["num_user_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[1]//span[@class='score']//text()").get()
        movie_item["num_critic_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[2]//span[@class='score']//text()").get()

        movie_item["num_oscar_nominations"] = content.xpath(".//li[@data-testid='award_information']/a[1]/text()").get()
        movie_item["num_wins"] = content.xpath("").get()
        movie_item["num_nominations"] = content.xpath("").get()

        movie_item["country"] = content.xpath(".//li[@data-testid='title-details-origin']/div[last()]//text()").get()
        movie_item["original_language"] = content.xpath(".//li[@data-testid='title-details-languages']/div[last()]//text()").get()

        yield movie_item
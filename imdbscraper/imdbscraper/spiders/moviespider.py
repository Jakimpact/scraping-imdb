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
        },
        'ITEM_PIPELINES': {
            'imdbscraper.pipelines.MovieCleaningPipeline': 600,
            'imdbscraper.pipelines.MoviePostgresPipeline': 700,
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
        movie_item["themes"] = content.xpath(".//div[@data-testid='genres']//text()").getall()
        movie_item["synopsis"] = content.xpath(".//p[@data-testid='plot']//text()").get()

        crews = content.xpath(".//p[@data-testid='plot']/following-sibling::div//li[@data-testid='title-pc-principal-credit']")
        for crew in crews:
            try:
                role = crew.xpath("./*[1]/text()").get().lower()
                if role in ("director", "directors"):
                    movie_item["directors"] = crew.xpath(".//li//text()").getall()
                if role in ("writer", "writers"):
                    movie_item["writers"] = crew.xpath(".//li//text()").getall()
                if role in ("star", "stars"):
                    movie_item["stars"] = crew.xpath(".//li//text()").getall()
            except:
                continue

        movie_item["metascore_rating"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[last()]//span[@class='score']//text()").get()
        movie_item["num_user_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[1]//span[@class='score']//text()").get()
        movie_item["num_critic_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[2]//span[@class='score']//text()").get()
        movie_item["num_oscar_nominations"] = content.xpath(".//li[@data-testid='award_information']/a[1]/text()").get()
        movie_item["num_wins"] = content.xpath(".//li[@data-testid='award_information']/div//text()").get()
        movie_item["num_nominations"] = content.xpath(".//li[@data-testid='award_information']/div//text()").get()
        movie_item["release_date"] = content.xpath(".//li[@data-testid='title-details-releasedate']/div[last()]//text()").get()
        movie_item["country"] = content.xpath(".//li[@data-testid='title-details-origin']/div[last()]//text()").get()
        movie_item["original_language"] = content.xpath(".//li[@data-testid='title-details-languages']/div[last()]//text()").get()
        movie_item["production_companies"] = content.xpath(".//li[@data-testid='title-details-companies']/div[last()]//text()").getall()
        movie_item["budget"] = content.xpath(".//li[@data-testid='title-boxoffice-budget']/div[last()]//text()").get()
        movie_item["ww_box_office"] = content.xpath(".//li[@data-testid='title-boxoffice-cumulativeworldwidegross']/div[last()]//text()").get()

        yield movie_item
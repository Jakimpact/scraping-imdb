import scrapy
from imdbscraper.items import ShowItem

class ShowspiderSpider(scrapy.Spider):
    name = "showspider"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/toptv/"]

    custom_settings = {
        'FEEDS': {
            'data/%(name)s/%(name)s_%(time)s.csv': {
                'format': 'csv',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        shows = response.xpath("//main//div[@data-testid='chart-layout-main-column']//ul[1]/li")

        for show in shows:
            relative_url = show.xpath(".//a[last()]/@href").get()
            if relative_url:
                show_url = "https://www.imdb.com/" + relative_url
                yield scrapy.Request(show_url, callback=self.parse_show_page)

    def parse_show_page(self, response):
        
        content = response.xpath("//main")
        show_item = ShowItem()

        show_item["url"] = response.url
        show_item["title"] = content.xpath(".//h1/span[@data-testid='hero__primary-text']/text()").get()
        show_item["years"] = content.xpath(".//h1/following-sibling::ul/li[2]//text()").get()
        show_item["public"] = content.xpath(".//h1/following-sibling::ul/li[3]//text()").get()
        show_item["episode_length"] = content.xpath(".//h1/following-sibling::ul/li[4]//text()").get()
        show_item["imdb_rating"] = content.xpath(".//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[1]/text()").get()
        show_item["num_imdb_raters"] = content.xpath(".//div[@data-testid='hero-rating-bar__aggregate-rating__score']/following-sibling::div/text()").get()
        show_item["themes"] = content.xpath(".//div[@data-testid='genres']//text()").getall()
        show_item["synopsis"] = content.xpath(".//p[@data-testid='plot']//text()").get()

        crews = content.xpath(".//p[@data-testid='plot']/following-sibling::div//li[@data-testid='title-pc-principal-credit']")
        for crew in crews:
            try:
                role = crew.xpath("./*[1]/text()").get().lower()
                if role in ("creator", "creators"):
                    show_item["creators"] = crew.xpath(".//li//text()").getall()
                elif role in ("star", "stars"):
                    show_item["stars"] = crew.xpath(".//li//text()").getall()
            except:
                continue
                
        show_item["num_user_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[1]//span[@class='score']//text()").get()
        show_item["num_critic_reviews"] = content.xpath(".//ul[@data-testid='reviewContent-all-reviews']/li[2]//span[@class='score']//text()").get()
        show_item["awards"] = content.xpath(".//li[@data-testid='award_information']/a[1]/text()").get()
        show_item["num_wins"] = content.xpath(".//li[@data-testid='award_information']/div//text()").get()
        show_item["num_nominations"] = content.xpath(".//li[@data-testid='award_information']/div//text()").get()
        show_item["num_seasons"] = content.xpath(".//select[@id='browse-episodes-season']/@aria-label").get()
        show_item["num_episodes"] = content.xpath(".//div[@data-testid='episodes-header']//span[last()]/text()").get()
        show_item["release_date"] = content.xpath(".//li[@data-testid='title-details-releasedate']/div[last()]//text()").get()
        show_item["country"] = content.xpath(".//li[@data-testid='title-details-origin']/div[last()]//text()").get()
        show_item["original_language"] = content.xpath(".//li[@data-testid='title-details-languages']/div[last()]//text()").get()
        show_item["production_companies"] = content.xpath(".//li[@data-testid='title-details-companies']/div[last()]//text()").getall()

        yield show_item
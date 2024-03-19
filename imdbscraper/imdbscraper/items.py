# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    original_title = scrapy.Field()
    year = scrapy.Field()
    public = scrapy.Field()
    length = scrapy.Field()
    imdb_rating = scrapy.Field()
    num_imdb_raters = scrapy.Field()
    themes = scrapy.Field()
    synopsis = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    metascore_rating = scrapy.Field()
    num_user_reviews = scrapy.Field()
    num_critic_reviews = scrapy.Field()
    num_oscar_nominations = scrapy.Field()
    num_wins = scrapy.Field()
    num_nominations = scrapy.Field()
    release_date = scrapy.Field()
    country = scrapy.Field()
    original_language = scrapy.Field()
    production_companies = scrapy.Field()
    budget = scrapy.Field() 
    ww_box_office = scrapy.Field()

    """
    Données supplémentaires à scrapper :
    - Affiche du film
    - détails user ratings (note + nombre)
    """

class ShowItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    years = scrapy.Field()
    public = scrapy.Field()
    episode_length = scrapy.Field()
    imdb_rating = scrapy.Field()
    num_imdb_raters = scrapy.Field()
    themes = scrapy.Field()
    synopsis = scrapy.Field()
    creators = scrapy.Field()
    stars = scrapy.Field()
    num_user_reviews = scrapy.Field()
    num_critic_reviews = scrapy.Field()
    awards = scrapy.Field()
    num_wins = scrapy.Field()
    num_nominations = scrapy.Field()
    num_seasons = scrapy.Field()
    num_episodes = scrapy.Field()
    release_date = scrapy.Field()
    country = scrapy.Field()
    original_language = scrapy.Field()
    production_companies = scrapy.Field()

    """
    Données supplémentaires à scrapper :
    - Affiche série
    - User ratings (note + nombre)
    """
    
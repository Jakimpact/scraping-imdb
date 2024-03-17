# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    original_title = scrapy.Field()
    imdb_rating = scrapy.Field()
    metascore_rating = scrapy.Field()
    themes = scrapy.Field()
    year = scrapy.Field()
    length = scrapy.Field()
    synopsis = scrapy.Field()
    directors = scrapy.Field()
    writers = scrapy.Field()
    stars = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    original_language = scrapy.Field()
    
    """
    Données supplémentaires à scrapper :
    - User ratings (note + nombre)
    - Users reviews / critics reviews ?
    - Nominated for oscars
    - Wins et nominations totales
    - Affiche du film
    - Date de sortie
    - Budget
    - Box office
    """

class ShowItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    original_title = scrapy.Field()
    imdb_rating = scrapy.Field()
    themes = scrapy.Field()
    beginning_year = scrapy.Field()
    ending_year = scrapy.Field()
    number_seasons = scrapy.Field()
    number_episodes = scrapy.Field()
    episode_length = scrapy.Field()
    synopsis = scrapy.Field()
    creators = scrapy.Field()
    stars = scrapy.Field()
    public = scrapy.Field()
    country = scrapy.Field()
    original_language = scrapy.Field()

    """
    Données supplémentaires à scrapper :
    - User ratings (note + nombre)
    - Users reviews / critics reviews ?
    - Primetime Emmys
    - Wins et nominations totales
    - Affiche série
    """
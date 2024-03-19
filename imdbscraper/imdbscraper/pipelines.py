# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import os
from dotenv import load_dotenv
import psycopg2

from itemadapter import ItemAdapter


load_dotenv()


class ImdbscraperPipeline:
    def process_item(self, item, spider):
        return item


class MoviesPostgresPipeline:

    def __init__(self):

        hostname = os.getenv("HOSTNAME")
        database = os.getenv("DATABASE")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")

        self.connection = psycopg2.connect(host=hostname, user=user, password=password, dbname=database)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            original_title TEXT,
            year INTEGER,
            public VARCHAR(255),
                         
            length TEXT,
            imdb_rating NUMERIC,
            num_imdb_raters INTEGER,
            themes TEXT,
            synopsis TEXT,
            directors TEXT[],
            writers TEXT[],
            stars TEXT[],
            metascore_rating NUMERIC,
            num_user_reviews INTEGER,
            num_critic_reviews INTEGER,
            num_oscar_nominations INTEGER,
            num_wins INTEGER,
            num_nominations INTEGER,
            release_date DATE,
            country TEXT,
            original_language TEXT,
            production_companies TEXT[],
            budget NUMERIC,
            ww_box_office NUMERIC
        )
        """)

    def process_item(self, item, spider):

        insert_statement = """=
            INSERT INTO movies (
                url, 
                title, 
                original_title, 
                year, 
                public, 
                length, 
                imdb_rating,
                num_imdb_raters, 
                themes, 
                synopsis, 
                directors, 
                writers, 
                stars,
                metascore_rating, 
                num_user_reviews, 
                num_critic_reviews,
                num_oscar_nominations, 
                num_wins, 
                num_nominations, 
                release_date,
                country, 
                original_language, 
                production_companies, 
                budget,
                ww_box_office
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        item_values = (
            item['url'], item['title'], item['original_title'], item['year'],
            item['public'], item['length'], item['imdb_rating'], item['num_imdb_raters'],
            item['themes'], item['synopsis'], item['directors'], item['writers'],
            item['stars'], item['metascore_rating'], item['num_user_reviews'],
            item['num_critic_reviews'], item['num_oscar_nominations'],
            item['num_wins'], item['num_nominations'], item['release_date'],
            item['country'], item['original_language'], item['production_companies'],
            item['budget'], item['ww_box_office']
        )
        
        try:
            self.cur.execute(insert_statement, item_values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
        return item

    def close_spider(self, item, spider):
        
        self.cur.close()
        self.connection.close()


class ShowPostgresPipeline:

    def __init__(self):

        hostname = os.getenv("HOSTNAME")
        database = os.getenv("DATABASE")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")

        self.connection = psycopg2.connect(host=hostname, user=user, password=password, dbname=database)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS shows(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            years TEXT[],
            public VARCHAR(255), 
            episode_length TEXT,
            imdb_rating NUMERIC,
            num_imdb_raters INTEGER,
            themes TEXT,
            synopsis TEXT,
            creators TEXT[],
            stars TEXT[],
            num_user_reviews INTEGER,
            num_critic_reviews INTEGER,
            awards INTEGER,
            num_wins INTEGER,
            num_nominations INTEGER,
            num_seasons INTEGER,
            num_episodes INTEGER,
            release_date DATE,
            country TEXT,
            original_language TEXT,
            production_companies TEXT[],
        )
        """)

    def process_item(self, item, spider):

        insert_statement = """=
            INSERT INTO movies (
                url, 
                title, 
                years, 
                public, 
                episode_length, 
                imdb_rating,
                num_imdb_raters, 
                themes, 
                synopsis, 
                creators,  
                stars,
                num_user_reviews, 
                num_critic_reviews,
                awards, 
                num_wins, 
                num_nominations,
                num_seasons,
                num_episodes,
                release_date,
                country, 
                original_language, 
                production_companies, 
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        item_values = (
            item['url'], item['title'], item['years'],
            item['public'], item['episode_length'], item['imdb_rating'], item['num_imdb_raters'],
            item['themes'], item['synopsis'], item['creators'],
            item['stars'], item['num_user_reviews'],
            item['num_critic_reviews'], item['awards'],
            item['num_wins'], item['num_nominations'], 
            item['num_seasons'], item['num_episodes'], item['release_date'],
            item['country'], item['original_language'], item['production_companies']
        )
        
        try:
            self.cur.execute(insert_statement, item_values)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
        return item

    def close_spider(self, item, spider):
        
        self.cur.close()
        self.connection.close()
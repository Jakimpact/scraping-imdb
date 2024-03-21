# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import re
import logging

import psycopg2

from imdbscraper.settings import HOSTNAME, PASSWORD, USER, DATABASE
from itemadapter import ItemAdapter


class MovieCleaningPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Transform url
        try:
            value = adapter.get("url")
            last_slash_index = value.rfind("/")
            cleaned_url = value[:last_slash_index + 1]
            adapter["url"] = cleaned_url
        except:
            pass

        # Transform length in minutes
        try:
            value = adapter.get("length")
            if 'h' in value:
                hours, minutes = map(int, value.replace('h', '').replace('m', '').split())
                total_min = hours * 60 + minutes
            else:
                total_min = int(value.replace('m', ''))
            adapter["length"] = total_min
        except: 
            pass

        # Transform num raters, num user reviews, num critic reviews in int
        try:
            reviews = ["num_imdb_raters", "num_user_reviews", "num_critic_reviews"]
            for review in reviews:
                value = adapter.get(review)
                if value:
                    if 'K' in value:
                        value = int(float(value.replace('K', '')) * 1000)
                    elif 'M' in value:
                        value = int(float(value.replace('M', '')) * 1000000)
                    else:
                        value = int(value)
                    adapter[review] = value    
        except:
            pass

        # Separate the num of wins and num of nominations
        try:
            value = adapter.get("num_wins")
            if value:
                matches = re.findall(r'(\d+)\s+wins?\s+&\s+(\d+)\s+nominations?\s+total', value)
                if matches:
                    num_wins, num_nominations = int(matches[0][0]), int(matches[0][1])
                else: 
                    num_wins, num_nominations = None, None
                adapter["num_wins"] = num_wins
                adapter["num_nominations"] = num_nominations
        except:
            pass

        # Remove what is inside the () for the release date
        try:
            value = adapter.get("release_date")
            if value:
                value = re.sub(r'\s*\(.*\)', '', value)
                adapter["release_date"] = value
        except:
            pass

        return item


class ShowCleaningPipeline(MovieCleaningPipeline):
    
    def process_item(self, item, spider):

        item = super().process_item(item, spider)

        adapter = ItemAdapter(item)

        # Transform length in minutes
        try:
            value = adapter.get("episode_length")
            if value:
                if 'h' in value:
                    hours, minutes = map(int, value.replace('h', '').replace('m', '').split())
                    total_min = hours * 60 + minutes
                else:
                    total_min = int(value.replace('m', ''))
                adapter["length"] = total_min
        except:
            pass

        # Transform num seasons in integer
        try:
            value = adapter.get("num_seasons")
            if value:
                if 'seasons' in value:
                    matches = re.match(r'^(\d+)\s+seasons?$', value.strip())
                    if matches:
                        adapter["num_seasons"] = int(matches.group(1))
                elif 'Season' in value:
                    matches = re.match(r'^(\d+)\s+Season$', value.strip())
                    if matches:
                        adapter["num_seasons"] = int(matches.group(1))
        except:
            pass
        
        return item
        

class MoviePostgresPipeline:

    def __init__(self):

        self.connection = psycopg2.connect(host=HOSTNAME, user=USER, password=PASSWORD, dbname=DATABASE)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS movies(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            original_title TEXT,
            year INTEGER,
            public VARCHAR(255),
            length INTEGER,
            imdb_rating DECIMAL,
            num_imdb_raters INTEGER,            
            themes TEXT[],
            synopsis TEXT,
            directors TEXT[],
            writers TEXT[],
            stars TEXT[],
            metascore_rating INTEGER,
            num_user_reviews INTEGER,
            num_critic_reviews INTEGER,
            num_oscar_nominations TEXT,
            num_wins INTEGER,
            num_nominations INTEGER,
            release_date DATE,
            country TEXT,
            original_language TEXT,
            production_companies TEXT[],
            budget TEXT,
            ww_box_office TEXT
        )
        """)

    def process_item(self, item, spider):

        # Check if the url is already in the database
        try:
            self.cur.execute("select * from movies where url = %s", (item['url'],))
            result = self.cur.fetchone()
        except:
            pass

        if result:
            spider.logger.warn("Item already in database: %s" % item['url'])
        
        else:

            insert_statement = """
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
                logging.error(f"Error inserting item into database: {e}")

        return item

    def close_spider(self, spider):
        
        self.cur.close()
        self.connection.close()


class ShowPostgresPipeline:

    def __init__(self):
        
        self.connection = psycopg2.connect(host=HOSTNAME, user=USER, password=PASSWORD, dbname=DATABASE)
        self.cur = self.connection.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS shows(
            id serial PRIMARY KEY,
            url VARCHAR(255),
            title TEXT,
            years TEXT,
            public VARCHAR(255), 
            episode_length INTEGER,
            imdb_rating DECIMAL,
            num_imdb_raters INTEGER,
            themes TEXT[],
            synopsis TEXT,
            creators TEXT[],
            stars TEXT[],
            num_user_reviews INTEGER,
            num_critic_reviews INTEGER,
            awards TEXT,
            num_wins INTEGER,
            num_nominations INTEGER,
            num_seasons INTEGER,
            num_episodes INTEGER,
            release_date DATE,
            country TEXT,
            original_language TEXT,
            production_companies TEXT[]
        )
        """)

    def process_item(self, item, spider):

        # # Check if the url is already in the database
        # try:
        #     self.cur.execute("select * from shows where url = %s", (item['url'],))
        #     result = self.cur.fetchone()
        # except:
        #     pass

        # if result:
        #     spider.logger.warn("Item already in database: %s" % item['url'])
        
        # Otherwise add the item to the database
        # else:

        insert_statement = """
            INSERT INTO shows (
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
                production_companies
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
            logging.error(f"Error inserting item into database: {e}")

        return item

    def close_spider(self, spider):
        
        self.cur.close()
        self.connection.close()
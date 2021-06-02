# -*- coding: utf-8 -*-

"""
Created on  Mon May 31 09:00:00 2021
@author: hugo.enrile.lacalle
@github: hugo-enrile
@email: hugoenrilelacalle@gmail.com
"""

from logging import NullHandler
from tarfile import NUL
import pandas as pd
import bs4 as BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from webdriver_manager import driver
from webdriver_manager.chrome import ChromeDriverManager

class Constants():
    """
    A class used to define constants
    """

    # Web prefix for TMDB
    WEB_PREFIX = "https://www.themoviedb.org/"

    # Supported languages
    ENGLISH = "en-EN"
    SPANISH = "es-ES"
    GERMAN = "de-DE"
    FRENCH = "fr-FR"
    ITALIAN = "it-IT"
    PORTUGUESE = "pt-PT"

    # Parts of the programs
    SEASON_CARD = "sc"


class TMDBScraper():
    """
    A class used to perform web scraping over the TMDB website to extract 
    the titles of episodes of a given TV Show.

    """

    # Webdriver options for the Selenium library
    webdriver_options = Options()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--disable-dev-shm-usage')

    def __init__(self):
        '''
        Initialize the class.

        Returns
        -------
        None.

        '''
        pass

    def select_language(input_language):
        '''
        Select the language code

        Parameters
        ----------
        input_language: String

        Returns
        -------
        language_code: String - Language Code or empty string

        '''

        if input_language.lower() == "english":
            language_code = Constants.ENGLISH
        elif input_language.lower() == "spanish":
            language_code = Constants.SPANISH
        elif input_language.lower() == "german":
            language_code = Constants.GERMAN
        elif input_language.lower() == "french":
            language_code = Constants.FRENCH
        elif input_language.lower() == "italian":
            language_code = Constants.ITALIAN
        elif input_language.lower() == "portuguese":
            language_code = Constants.PORTUGUESE
        else:
            language_code = ""
        return language_code
    
    def get_id(driver, title, language):
        '''
        Extract TMDB unique id used to identify each TV Show

        Parameters
        ----------
        driver: Selenium
        title: String
        language: String
        part: String

        Returns
        -------
        id = Integer

        '''

        url = Constants.WEB_PREFIX + "search/tv?query= " + title + "&language=" + language
        driver.get(url)
        page_source = driver.page_source
        try:
            html_soup = BeautifulSoup.BeautifulSoup(page_source, 'html.parser')
            html_title = html_soup.find('div', class_ = 'title').h2.text
            print('Title: ' + html_title)
            id_tmdb_num = html_soup.find('div', class_ = 'title').find('a').get('href')
            m = re.search('(tv\/)(.+?)(\?)', str(id_tmdb_num))
            id_tmdb = m.group(2)
            return id_tmdb
        except:
            print("Failed, probably " + title + " is not a TV Show.\n\n")
            return None

    def get_season(driver, id, language):
        '''
        Extract the number of seasons 

        Parameters
        ----------
        driver: Selenium
        id: Integer
        language: String

        Returns
        -------
        seasons = Integer

        '''

        url = Constants.WEB_PREFIX + "tv/" + id + "?language=" + language
        print(url)
        driver.get(url)
        page_source = driver.page_source
        try:
            soup = BeautifulSoup.BeautifulSoup(page_source, 'html.parser')
            html = soup.find('div', class_ = 'season card')
            last_season = html.h2.text
            m = re.search('( )(.+?)', str(last_season))
            seasons = m.group(2)
            print(seasons + " seasons")
            print("-----------------------\n\n")
            return seasons
        except:
            print("Failed, probably is not a TV Show.\n\n")
    
    def get_episodes(driver, seasons, id, language):
        '''
        Print the title of the episodes of the different seasons of the TV Show.

        Parameters
        ----------
        driver: Selenium
        seasons: Integer
        id: Integer
        language: String

        Returns
        -------
        None.

        '''

        for season in range(int(seasons)):
                print("Season " + str(season+1))
                url = "https://www.themoviedb.org/tv/" + id + "/season/" + str(season+1) + "?language=" + language
                driver.get(url)
                page_source = driver.page_source
                try:
                    html_soup = BeautifulSoup.BeautifulSoup(page_source, 'html.parser')
                    episode = html_soup.find_all('div', class_ = 'wrapper')
                    episode_name = []
                    for container in episode:
                        name = container.h3.text
                        if name not in episode_name:
                            episode_name.append(name)
                    df = pd.DataFrame({'EPISODES': episode_name})
                    print(df)
                    print("\n\n")
                except:
                    print("Season " + str(season+1) + " is not available.\n\n")

    if __name__ == '__main__':
        input_title = input('Introduce the title of a TV show: ')
        input_language = ""
        while input_language ==  "":
            input_language = input('Introduce a language: ')
            if input_language == "":
                print("Selected language is not currently available, please try it again.\n")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=webdriver_options)
        print("Searching " + input_title + "...\n")
        language_code = select_language(input_language)
        id = get_id(driver, input_title, language_code)
        seasons = get_season(driver, id, language_code)
        get_episodes(driver, seasons, id, language_code)
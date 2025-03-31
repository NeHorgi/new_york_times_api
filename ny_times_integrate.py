import logging
import os
from typing import Generator

import requests
from dotenv import load_dotenv
from requests import Session

from constants import config
from ny_times_article import NYTimesArticle

load_dotenv()


class NewYorkTimesSource:
    """
    Integration with New York Times API.
    """

    def __init__(self, api_key: str):
        self.__api_key = api_key
        self.__session = None

    @property
    def session(self) -> Session:
        """
        Initializes and returns a requests session with the API key.

        :return: Requests session.
        """
        if self.__session is None:
            logging.info(f"Creating a session.")
            self.__session = requests.Session()
            self.__session.params = {"api-key": self.__api_key}
        return self.__session

    def _get(self, api: str, endpoint: str, params: dict) -> dict[str, str]:
        """
        Sends a GET request to the specified API endpoint.
        Method also handles an exception with too many request.

        :param api: The API section to query.
        :param endpoint: The specific API endpoint.
        :param params: Dictionary of query parameters.

        :return: JSON response as a dictionary.
        """
        url = config.base_url + api + endpoint
        logging.info(f"Trying to send a request for {url} with params {params}")
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            logging.info(f"The request was send.")
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                logging.warning("Too many requests, got an 429 Error. Try again later.")
                return {}
            else:
                logging.error(f"HTTPError: {e}")
                return {}
        except Exception as e:
            logging.error(f"Error while trying to send a request: {e}")
            return {}

    def get_articles(self, batch_size: int, query: str = None) -> Generator[list[NYTimesArticle], None, None]:
        """
        Get articles from NYTimes, with specific query if it exists.
        Method returns a generator what yields batches, by given batch size, of data with NYTimes articles.

        :param batch_size: Number of articles per batch.
        :param query: Optional search query.

        :yield: List of batches with given batch size of NYTimesArticle objects.
        """
        logging.info(f"Getting articles with: batch_size - {batch_size}, query - {query}")
        page = 0
        buffer = []
        while True:
            params = {"page": page}
            if query:
                params["q"] = query
            response = self._get(api=config.article_search_api, endpoint="articlesearch.json", params=params)
            articles = [NYTimesArticle(
                web_url=article["web_url"],
                author=article["byline"],
                id=article["_id"],
                pub_date=article["pub_date"],
                article_data=NYTimesArticle.get_flatten_dict(article)
            ) for article in response.get("response", {}).get("docs", [])]
            if not articles:
                logging.info(f"There is no more articles.")
                break

            buffer.extend(articles)

            while len(buffer) >= batch_size:
                yield buffer[:batch_size]
                buffer = buffer[batch_size:]

            page += 1
        if buffer:
            yield buffer


NYTimeSource = NewYorkTimesSource(os.getenv("API_KEY"))

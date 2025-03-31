from dataclasses import dataclass


@dataclass
class NYTimesArticle:
    """
    Represents a New York Times article with metadata and content.

    Attrs:
    web_url - URL of the article
    id - Unique article identifier
    author - Author of the article
    pub_date - Publication date of the article
    article_data - Dictionary containing article content and metadata
    """
    web_url: str
    id: str
    author: str
    pub_date: str
    article_data: dict

    @staticmethod
    def get_flatten_dict(dictionary: dict, parent_key: str = "") -> dict[str, str]:
        """
        Flattens a nested dictionary into a single-level dictionary with dot-separated keys.

        :param dictionary: The dictionary to flatten.
        :param parent_key: The base key for recursion (default is an empty string).

        :return: A flattened dictionary where nested keys are represented using the delimiter.
        """
        result = {}
        for key, value in dictionary.items():
            new_key = f"{parent_key}.{key}" if parent_key else key
            if isinstance(value, dict):
                result.update(NYTimesArticle.get_flatten_dict(value, new_key))
            else:
                result[new_key] = value
        return result

    def get_schema(self) -> list[str]:
        """
        Get the schema of the article's `article_data` dictionary.

        :return: A list of keys present in the `article_data` dictionary.
        """
        return list(self.article_data.keys())

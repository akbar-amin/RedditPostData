import requests
import jmespath
from collections import OrderedDict
from urllib.parse import urlencode
from .utils import buildExpr, defaultExpr

__all__ = ["Reddit"]

class Reddit:
    def __init__(self, subreddit: str, *keys) -> None:
        """
        Scrape Reddit posts via HTTP requests to the non-OAuth Reddit API.

        Args:
            subreddit: the name of the subreddit (without "r/")
            keys: keywords to parse from post data (see ``utils.attributes``)
                    Defaults to all items listed in ``utils.attributes``

        Example usage:

        Get data from 25 of the newest posts.
        ```python3
            subreddit = Reddit("wallstreetbets")
            data = subreddit.sort(by="new", limit=25)
        ```
        """
        if keys:
            self.expression = jmespath.compile(buildExpr(*keys))
        else:
            self.expression = jmespath.compile(defaultExpr())
        self.subreddit = subreddit  


    def request(self, URL: str) -> OrderedDict:
        """
        Send an "GET" HTTP request and parse the results.

        Args:
            URL: a formatted request URL pointing to a JSON webpage
        """
        response = requests.get(URL, timeout = (10, 10), headers = {"User-Agent": "Mozilla/5.0"})
        print(f"[{response.status_code}] {response.url}")
        
        return self.expression.search(response.json(), 
                        jmespath.Options(dict_cls = OrderedDict))

    def sort(self, by: str, limit: int = 25, count: int = 0, sr_details: bool = True,
                            t: str = None, before: str = None, after: str = None) -> list:
        """
        Retrieve posts by a sorting method.

        Args:
            by: a sorting method ("best", "hot", "new", "top", "controversial", "rising", "random", 
                                    "sidebar", "sticky", "about", "search", "stylesheet")
            limit: the maximum number of items to return in this slice of the listing
            count: the number of items already seen in this listing (used with before/after)
            t: return posts for a specific time period ("hour", "day", "week", "month", "year", "all")
            sr_details: expand subreddit details (recommended to leave as "True")
            before, after: the fullname (unique id) of the post to use as endpoints for a range
        """
        kwargs = {k:v for k,v in locals().items() if isinstance(v, (str, int, bool))}
        method = kwargs.pop("by").lower()
        URL = f"https://www.reddit.com/r/{self.subreddit}/{method}.json?{urlencode(kwargs)}"

        return self.request(URL)

    def byId(self, *fullnames) -> list:
        """
        Retrieve posts by their unique identifier.

        Args:
            fullnames: the unique id corresponding to a Reddit item
                        (https://www.reddit.com/dev/api#fullnames)

        Note: 
            All post-related identifiers should have "t3" as their prefix.
        ```text
            For the following post:
                https://www.reddit.com/r/wallstreetbets/comments/lnqgz8/gme_yolo_update_feb_19_2021/

            The identifier is "lnqgz8" 
            Therefore, the fullname is "t3_lnqgz8" 
        ```

        Example usage:
        ```python3
            subreddit.byId("t3_lnqgz8", "t3_lo4qu6", ...)
        ```
        """
        URL = f"https://www.reddit.com/by_id/{','.join(fullnames)}.json" 
        return self.request(URL)



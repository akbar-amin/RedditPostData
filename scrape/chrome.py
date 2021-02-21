
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
from datetime import date
from pathlib import Path
from typing import Union

__all__ = ["WebReddit"]

class WebReddit:
    def __init__(self, subreddit: str, excpath: Union[Path, str] = "chromedriver") -> None:
        """
        Alternative approach to Reddit link-scraping via Selenium webdriver (Chrome).

        Args:
            subreddit: the name of the subreddit (without "r/")
            excpath: path or environment variable pointing to a chromedriver executable 

        Example usage:

        Get the first 100 links from the top posts and save the links to text file.
        ```python3
            scraper = WebReddit("wallstreetbets")
            scraper.grab(sorting = "top", N = 100, save = True)
        ```
        """
        self.subreddit = subreddit
        self.excpath = excpath
        self.links = set()

    @property
    def options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--log-level=3")
        options.add_argument("--headless")
        return options

    @property
    def outdir(self) -> Path:
        folder = (Path(__file__).parents[1] / Path(f"data/{self.subreddit}")).resolve()
        folder.mkdir(parents = True, exist_ok = True)
        return folder

    @staticmethod
    def scroll(chrome) -> int:
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return chrome.execute_script("return document.body.scrollHeight")

    @staticmethod
    def parse(chrome) -> list:
        soup = BeautifulSoup(chrome.page_source, "lxml")
        elements = soup.find_all("a", class_ = "comments may-blank")
        return list(map(lambda tag: tag.get("href"), elements))

    def webpage(self, *args):
        return "/".join(["https://www.reddit.com", "r", self.subreddit, *args, ".compact"])

    def grab(self, sorting: str, N: int = 100, save: bool = False) -> None:
        chrome = Chrome(self.excpath, options = self.options) 
        chrome.get(self.webpage(sorting))
        items = set()
        try:
            prev = 0
            while len(items) < N:
                current = self.scroll(chrome)
                if current > prev:
                    items.update(self.parse(chrome))
                    prev = current
        finally:
            chrome.quit()
            items = list(items)
            if len(items) > N:
                items = items[:N]
            if save:
                outfile = Path(f"{sorting.upper()}_{date.today().strftime('%m_%d_%y')}.txt")
                (self.outdir / outfile).write_text("\n".join(items))
                print(f"Saved {len(items)} links to {str(outfile)}")
            else:
                print(f"Updated {len(items)} links")
            self.links.update(items)
            print(f"Total unique links: {len(self.links)}")


### About
A tool for retrieving post data from Reddit and optionally writing the results into Google Sheets.

The motivation for this project was to find some way to confront post data directly without needing to register an application with Reddit's API. 

While there are plenty of libraries that provide easy interaction with Reddit's OAuth API, much of the time it feels like I'm fighting with these libraries to get the data I want. Personally, I find it easier and more effecient to confront the data source directly at the cost of convenience that external libraries provide. Additionally, the motivation for this was to only get post data, specifically for a school project. 

The primary scraping method is done via HTTP requests; however, an additional method is implemented with Selenium. This was done just for fun, as I genuinely enjoy web automation. 

Read [here](https://www.reddit.com/dev/api) for more information on the source of the data.

### Example
[Data Output (Google Sheets)](https://docs.google.com/spreadsheets/d/e/2PACX-1vQ80MZ_M92oxBQKX_lAlYrpKkQ2BcXYHlFyTK3zpnrABmzjEFjhwqOZdo30y9XTn7z34edWiCg-7LGn/pubhtml)

```python3

  subreddit = Reddit("wallstreetbets")        
  spreadsheet = Sheets("Reddit Scrape Data")
  data = subreddit.sort(by="top",limit=50)
  spreadsheet.new("Top50")
  spreadsheet.write(data)
```
*Refer to [main.py](https://github.com/akbar-amin/RedditPostData/blob/main/main.py) for a more in-depth running example.*

### Dependencies

Required:
```text
requests==2.24.0
jmespath==0.10.0
pandas==1.1.4
gspread==3.6.0
```

Optional:
```text
selenium==3.141.0
beautifulsoup4==4.9.3
python-dotenv==0.15.0
```

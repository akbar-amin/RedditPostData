import time 
from itertools import product 
from scrape import Reddit, Sheets

#################################################################################
#   Make sure to have the path to your google service account credentials set   #
#   if you plan on using Sheets. You can set these variables with a '.env' file #
#   or with the 'os' module.                                                    #
#                                                                               #
#   The environmental variables should be "CREDENTIALS" and/or "SPREADSHEET".   #
#################################################################################

subreddit = Reddit("wallstreetbets")        # scrape r/wallstreetbets
spreadsheet = Sheets("Reddit Scrape Data")  # set the spreadsheet to write to 

methods = ("best", "hot", "new", "top", "controversial", "rising")    # examples of sorting methods
periods = ("day", "week", "month", "year", "all")                     # examples of time periods
n = 100                                                               # the number of posts to fetch (limit)


for m, p in product(methods, periods):  # iterate over all combinations of 'methods' and 'periods'
    data = subreddit.sort(m, n, t = p)  # fetch 'n' posts sorted by 'm' over 'p' time interval 
    ws = f"{m.title()}{n}{p.title()}"   # worksheet name to write into 
    spreadsheet.new(ws)                 # create the worksheet
    spreadsheet.write(data)             # write the data

    time.sleep(1.5)                     # handle google quota timeouts


# Console Output:
# [200] https://www.reddit.com/r/wallstreetbets/best.json?limit=100&count=0&sr_details=True&t=day
# [200] https://www.reddit.com/r/wallstreetbets/best.json?limit=100&count=0&sr_details=True&t=week
# [200] https://www.reddit.com/r/wallstreetbets/best.json?limit=100&count=0&sr_details=True&t=month
# [200] https://www.reddit.com/r/wallstreetbets/best.json?limit=100&count=0&sr_details=True&t=year
# [200] https://www.reddit.com/r/wallstreetbets/best.json?limit=100&count=0&sr_details=True&t=all
#                                     ... (truncated) ...  
# [200] https://www.reddit.com/r/wallstreetbets/rising.json?limit=100&count=0&sr_details=True&t=day
# [200] https://www.reddit.com/r/wallstreetbets/rising.json?limit=100&count=0&sr_details=True&t=week
# [200] https://www.reddit.com/r/wallstreetbets/rising.json?limit=100&count=0&sr_details=True&t=month
# [200] https://www.reddit.com/r/wallstreetbets/rising.json?limit=100&count=0&sr_details=True&t=year
# [200] https://www.reddit.com/r/wallstreetbets/rising.json?limit=100&count=0&sr_details=True&t=all

# Google Sheets Output [Public]:
# https://docs.google.com/spreadsheets/d/e/2PACX-1vQ80MZ_M92oxBQKX_lAlYrpKkQ2BcXYHlFyTK3zpnrABmzjEFjhwqOZdo30y9XTn7z34edWiCg-7LGn/pubhtml

### About

- This is a variant of scrapy-googlenews web crawler where sentiment analysis is added using TextBlob library.
- Web crawler is still built using scrapy. 
- The parameter need to be passed inside the code (i.e. **google_sentiment\google_sentiment\spiders\sentiment.py**) from line 14 to line 19 instead of through command line.
```
    # Change Parameter Here
    startDate =  datetime.date(2020, 1, 3)
    endDate = datetime.date(2020, 1, 3)
    delta = datetime.timedelta(days=1)
    country = "china"
    query = "semiconductor"
```

- The crawl works through looping the date range from `startDate` variable to `endDate` variable as per defined on line 15 and line 16 of `sentiment.py`

- Latest command to crawl is simply: `scrapy crawl sentiment -o <filename.csv>`

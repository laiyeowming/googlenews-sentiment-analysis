import scrapy
from google_sentiment.items import GoogleSentimentItem
from scrapy.loader import ItemLoader
import nltk
from newspaper import Article
import datetime
from textblob import TextBlob


class gSpider(scrapy.Spider):
    nltk.download('punkt')
    name= 'sentiment'

    # Change Parameter Here
    startDate =  datetime.date(2020, 1, 3)
    endDate = datetime.date(2020, 1, 3)
    delta = datetime.timedelta(days=1)
    country = "china"
    query = "semiconductor"

    # Crawling start here    
    def start_requests(self):
        while self.startDate <= self.endDate:
            activeDate = self.startDate.strftime("%m/%d/%Y")
            yield scrapy.Request(f'https://www.google.com/search?q={self.country}+{self.query}&rlz=1C1ONGR_enSG933SG933&tbs=cdr:1,cd_min:{activeDate},cd_max:{activeDate},sbd:1&tbm=nws&sxsrf=ALeKk01aflpQNP1ZZ_T4be6c1j0AaGca-g:1629088758656&source=lnt&sa=X&ved=2ahUKEwiVoJHG3LTyAhUIA3IKHUJTA3gQpwV6BAgHECw&biw=1920&bih=969&dpr=1')
            self.startDate += self.delta

    def parse(self, response):


        for articles in response.css('div.dbsr'):

            # summarizer start here
            url = articles.css('a::attr(href)').get()

            try:
                article = Article(url)
                article.download()
                article.parse()
                article.nlp()
                summary = article.summary
                # This is the part where sentiment analysis is added
                fullText = article.text
                analysis = TextBlob(fullText)
                sentiment = analysis.polarity
                subjective = analysis.subjectivity

            except:
                summary = articles.css('div.Y3v8qd::text').get()
                # This is the part where sentiment analysis is added
                analysis = TextBlob(summary)
                sentiment = analysis.polarity
                subjective = analysis.subjectivity

            # summarizer end here

            l = ItemLoader(item = GoogleSentimentItem(), selector=articles)

            l.add_css('title', 'div.JheGif.nDgy9d')
            l.add_value('excerpt', summary)
            l.add_css('source','div.XTjFC.WF4CUc')
            l.add_css('date', 'span.WG9SHc span')
            l.add_value('query', self.query)
            l.add_value('country', self.country)
            l.add_css('link','a::attr(href)')
            l.add_value('sentiment', sentiment)
            l.add_value('subjective', subjective)

            yield l.load_item()


        # nextPage = response.css('[id="pnnext"]').attrib['href']
        # nextLink = "https://google.com" + nextPage

        # if nextPage is not None:
        #     yield response.follow(nextLink, callback=self.parse)
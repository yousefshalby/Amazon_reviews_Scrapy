import scrapy
from scrapy.crawler import CrawlerProcess
import json


class Reviews(scrapy.Spider):
    
    name = "amazon"
    
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'amzon.csv',
    }
    
    headers = {
        'DOWNLOAD_DELAY': 2,                     
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1  ,
        "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36x-requested-with: XMLHttpRequest",
        "accept":" text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language":" en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie":'session-id=131-6627789-7693030; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:EG"; ubid-main=134-5405073-4206837; lc-main=en_US; session-token=p9bvJNyxHIfJszCRIZYxoVEwAyiRr9uyIE551xpt5WvY17POF5h9b14MRK8UrFXUV98ipUJ1tmWW8HO3QVzoXoEhH42j0rBWN8h/HqUbr6lo4e+9WrOAECRBwCOEO5iGV/zul1KlLSc3onwyuJcSY8yIYCqpy5aJqnBErOV4DfLENemh6o5LiS1CrD5VKfps; csm-hit=tb:s-EZ6VBZK4009J398076R1|1619311828908&t:1619311829985&adb:adblk_yes',
        "dnt":" 1",
        "downlink": "4.6",
        "ect": "4g",
        "pragma": "no-cache",
        "rtt": "100",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        "sec-ch-ua-mobile":" ?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode":" navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    }
    
    def start_requests(self):
        url = "https://www.amazon.com/product-reviews/B07VMB5L3C/ref=cm_cr_getr_d_paging_btm_next_"
        for page in range(1, 4):
            next_page = url +str(page)+"?pageNumber="+str(page)
            yield scrapy.Request(url= next_page, headers= self.headers, callback= self.parse)
       

    def parse(self, response):
        for review in response.css('[data-hook="review"]'):
                item={
                    "name" : ''.join(review.css('.a-profile-content').css("span.a-profile-name ::text").extract()),
                    "titles" :''.join(review.css("a[data-hook='review-title']").css("span ::text").extract()),
                    "stars" : ''.join(review.css("i[data-hook='review-star-rating']").css("span.a-icon-alt ::text").extract()),
                    "review" : ''.join(review.css(".review-text-content").css("span ::text").extract()).replace("\n",'').strip(),        
                }

                yield item

                print(json.dumps(item, indent=2))

if __name__ == '__main__':
    scraper = CrawlerProcess()  
    scraper.crawl(Reviews)
    scraper.start()          
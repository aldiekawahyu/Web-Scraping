from myscraper.myscraper.spiders.okezone_edukasi import OkezoneEdukasiSpider
from scrapy.crawler import CrawlerProcess
from datetime import datetime


if __name__ == '__main__':
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f'../results/{timestamp}-Result_OkezoneEdukasi.json'
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': filename
    })
    process.crawl(OkezoneEdukasiSpider)
    process.start()
    process.stop()

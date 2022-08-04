import scrapy


class OkezoneEdukasiSpider(scrapy.Spider):
    name = 'okezone_edukasi'
    allowed_domains = ['edukasi.okezone.com']
    start_urls = ['http://edukasi.okezone.com/']

    def parse(self, response):
        headers = response.xpath('//h2')

        for header in headers:
            title = ''.join(header.xpath('.//text()').extract())
            link = header.xpath('./a/@href').get()

            item = {'judul': title, 'link': [link]}
            request = scrapy.Request(link, callback=self.parse_article)
            request.meta['item'] = item

            yield request

    def parse_article(self, response):
        article = ''.join(response.xpath("//div[contains(@id, 'contentx')]/p//text()").extract())
        date = ' '.join(response.xpath("//div[contains(@class, 'namerep')]/b//text()").get().split()[1:4])
        total_page = int(response.xpath("//div[contains(@class, 'second-paging')]/text()").get())

        item = response.meta['item']
        item['artikel'] = article
        item['tanggal'] = date

        if total_page == 1:
            yield item

        for i in range(2, total_page + 1):
            item['link'].append(str(i).join(item['link'][-1].rsplit(item['link'][-1][-1:], 1)))
            request = scrapy.Request(item['link'][-1], callback=self.parse_article_cont)
            request.meta['item'] = item

            if i < total_page:
                request.meta['Break'] = False
            else:
                request.meta['Break'] = True

            yield request

    @staticmethod
    def parse_article_cont(response):
        paragraphs = response.xpath("//div[contains(@id, 'contentx')]/p//text()").extract()
        new_paragraphs = []
        for paragraph in paragraphs:
            new_paragraphs.append(paragraph.replace("\n", ""))
        article = '\n\n'.join(new_paragraphs)

        item = response.meta['item']
        item['artikel'] = item['artikel'] + article

        if response.meta['Break']:
            yield item

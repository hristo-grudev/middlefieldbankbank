import scrapy

from scrapy.loader import ItemLoader

from ..items import MiddlefieldbankbankItem
from itemloaders.processors import TakeFirst
import requests

url = "https://www.middlefieldbank.bank/modules/blog/ajax/blog-list-items.php"

payload="ourPage=1&resultsCount=9999999&URL=&slug="
headers = {
  'authority': 'www.middlefieldbank.bank',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': '*/*',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://www.middlefieldbank.bank',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.middlefieldbank.bank/blog',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': 'PHPSESSID=4i6avfcnqng39lfq4s4ool9vup; _ga=GA1.2.989001921.1617795256; _gid=GA1.2.175725362.1617795256; _aeaid=818e4808-743f-43d6-b768-c88fcf3a7cca; aeatstartmessage=true; _dc_gtm_UA-126906227-1=1; _dc_gtm_UA-126906227-2=1; _dc_gtm_UA-159815663-1=1; _gat_UA-126906227-1=1; Retarget=%2C43%2C%2C%2C45%2C'
}


class MiddlefieldbankbankSpider(scrapy.Spider):
	name = 'middlefieldbankbank'
	start_urls = ['https://www.middlefieldbank.bank/blog']

	def parse(self, response):
		data = requests.request("POST", url, headers=headers, data=payload)
		raw_data = scrapy.Selector(text=data.text)

		post_links = raw_data.xpath('//a[contains(@class,"link-arrow")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="article-header"]/h2/text()').get()
		description = response.xpath('//div[@class="text-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date"]/text()').get()

		item = ItemLoader(item=MiddlefieldbankbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()

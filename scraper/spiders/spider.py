import re

import demjson
import scrapy
from scrapy.http import Response

from scraper.helpers import CustomJSON
from scraper.word import Word

REGEX = r'window\.INITIAL_STATE\s+=\s+\{([\s\S]+)\};'


class ThesaurusSpider(scrapy.Spider):
    name = 'thesaurus'
    start_urls = ['https://www.thesaurus.com/browse/lock%20up']
    download_delay = 1

    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = set()

    def parse(self, response: Response, **kwargs):
        for script in response.xpath('//script/text()').getall():
            # Look for the specific script tag we want
            if 'INITIAL_STATE' in script:
                # Extract the interesting part from the script tag
                m = re.match(r'window\.INITIAL_STATE\s+=\s+({[\s\S]+});', script)

                # Decode it properly, handling annoying unicode escapes and nonsense from the site renderer
                custom_demjson = CustomJSON(json_options=demjson.json_options(compactly=False))
                decoded = custom_demjson.decode(m.group(1), encoding='unicode-escape')

                # Write a proper valid JSON file out
                # with open('example.json', 'w', encoding='utf-8') as file:
                #     file.write(custom_demjson.encode(decoded))

                raw_data = decoded['searchData']
                word = Word.from_raw(data=raw_data)

                urls = word.get_urls()
                new = urls - self.queue
                self.queue.update(new)

                if len(new) > 0:
                    print(f'Found {len(new)} more URLs.')
                return response.follow_all(new)

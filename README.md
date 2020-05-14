# Amazon Laptops Scrapy spider
This spider allows you crawl data about laptops from amazon.

Firstly, you need to get links, using AmazonLink spider:

```bash
scrapy crawl amazon_spider -o output.json
```

Then run AmazonData spider, to get information about laptops.

```bash
scrapy crawl amazon_laptops
```

Note: In settings file you need to determine path to proxy list in format - "ip:port".
```python
ROTATING_PROXY_LIST_PATH = 'path/to/proxy.txt'
```

Also, you will need to install a [scrapy-rotating-proxies](https://pypi.org/project/scrapy-rotating-proxies/)

! If you don't use proxies, amazon will ban your ip after 100 requests.

!! Don't use public proxies, that will lead you to get ban from amazon too.

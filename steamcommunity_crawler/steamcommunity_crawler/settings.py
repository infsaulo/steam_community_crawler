import os.path

BOT_NAME = 'steamcommunity_crawler'

SPIDER_MODULES = ['steamcommunity_crawler.spiders']
NEWSPIDER_MODULE = 'steamcommunity_crawler.spiders'
COOKIES_ENABLED = False
CONCURRENT_REQUESTS = 50
DEPTH_STATS_VERBOSE = True
# Depth first search
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'steamcommunity_crawler (+http://www.yourdomain.com)'
LOG_FILE = os.path.expanduser("~/logs/steamcommunity_crawler.log")
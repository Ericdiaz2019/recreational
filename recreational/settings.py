# Scrapy settings for the recreational project

BOT_NAME = "recreational"
SPIDER_MODULES = ["recreational.spiders"]
NEWSPIDER_MODULE = "recreational.spiders"

# Enable Playwright as the download handler for HTTP and HTTPS
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
LOG_LEVEL = 'INFO'

# Enable robots.txt compliance
ROBOTSTXT_OBEY = True

# Limit the number of concurrent requests and contexts for Playwright
#CONCURRENT_REQUESTS = 5
#PLAYWRIGHT_MAX_CONTEXTS = 5

# Download delay to reduce load on server
DOWNLOAD_DELAY = 2  # Adjust as needed

# Retry failed requests automatically (helpful with proxies)
RETRY_ENABLED = True
RETRY_TIMES = 5  # Number of retries for failed requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]  # Retry on server errors

# Playwright-specific settings
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 60000  # Set to 60 seconds
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
}

# Throttle settings for polite scraping
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2  # Initial delay before requests
AUTOTHROTTLE_MAX_DELAY = 30  # Maximum delay in case of high latencies
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable HTTP cache for faster debugging
HTTPCACHE_ENABLED = False  # Set to True if caching responses is desirable
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]

# Set settings whose default value is deprecated
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
FEED_EXPORT_ENCODING = "utf-8"

from crawler.WexAppCrawler import WexAppCrawler

# Update tree info
crawler = WexAppCrawler('.', '.wex/ai/data/tree.yml')
crawler.build()


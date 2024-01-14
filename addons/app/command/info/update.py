from src.core.Kernel import Kernel
from addons.app.decorator.app_command import app_command
from addons.ai.src.crawler.AppCrawler import CrawlerTreeItem
from addons.ai.src.crawler.WexAppCrawler import WexAppCrawler


@app_command(help="Description")
def app__info__update(kernel: Kernel, app_dir: str) -> CrawlerTreeItem:
    crawler = WexAppCrawler(app_dir, '.wex/ai/data/tree.yml')

    return crawler.build()

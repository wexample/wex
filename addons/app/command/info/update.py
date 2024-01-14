from addons.ai.src.crawler.AppCrawler import CrawlerTreeItem
from addons.ai.src.crawler.WexAppCrawler import WexAppCrawler
from addons.app.decorator.app_command import app_command
from src.core.Kernel import Kernel


@app_command(help="Description")
def app__info__update(kernel: Kernel, app_dir: str) -> CrawlerTreeItem:
    return WexAppCrawler(app_dir, ".wex/ai/data/tree.yml").build()

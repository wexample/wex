from addons.ai.src.crawler.app_crawler import CrawlerTreeItem
from addons.ai.src.crawler.python_app_crawler import PythonAppCrawler


class WexAppCrawler(PythonAppCrawler):
    def cleanup_tree(self, tree: CrawlerTreeItem) -> CrawlerTreeItem:
        tree = super().cleanup_tree(tree)

        if not tree["children"]:
            return tree

        # Useless folder
        tree["children"]["tmp"] = {"type": "dir", "status": "hidden"}
        tree["children"]["wex.egg-info"] = {"type": "dir", "status": "hidden"}

        # Security tokens
        tree["children"][".env"] = {"type": "file", "status": "hidden"}

        return tree

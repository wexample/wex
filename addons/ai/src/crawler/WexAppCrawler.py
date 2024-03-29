from addons.ai.src.crawler.AppCrawler import CrawlerTreeItem
from addons.ai.src.crawler.PythonAppCrawler import PythonAppCrawler


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

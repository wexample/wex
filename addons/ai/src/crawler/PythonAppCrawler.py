from addons.ai.src.crawler.AppCrawler import AppCrawler, CrawlerTreeItem


class PythonAppCrawler(AppCrawler):
    def tree_remove(self, tree: CrawlerTreeItem, file_name: str) -> None:
        if "children" not in tree:
            return

        for key, value in tree["children"].items():
            self.tree_remove(value, file_name)

        if file_name in tree["children"]:
            del tree["children"][file_name]

    def cleanup_tree(self, tree: CrawlerTreeItem) -> CrawlerTreeItem:
        tree = super().cleanup_tree(tree)
        self.tree_remove(tree, '__pycache__')
        return tree

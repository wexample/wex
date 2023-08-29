from core.PythonAppCrawler import PythonAppCrawler


class WexAppCrawler(PythonAppCrawler):
    def get_source_tree(self):
        tree = super().get_source_tree()

        # Useless folder
        tree['tmp'] = {}
        tree['wex.egg-info'] = {}

        return tree

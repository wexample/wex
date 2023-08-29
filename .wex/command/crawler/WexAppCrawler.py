from crawler.PythonAppCrawler import PythonAppCrawler


class WexAppCrawler(PythonAppCrawler):
    def cleanup_tree(self, tree):
        tree = super().cleanup_tree(tree)

        # Useless folder
        tree['children']['tmp'] = {}
        tree['children']['wex.egg-info'] = {}

        # Security tokens
        tree['children']['.env'] = {'status': 'hidden'}

        return tree

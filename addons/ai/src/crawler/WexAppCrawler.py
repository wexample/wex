from addons.ai.src.crawler.PythonAppCrawler import PythonAppCrawler

class WexAppCrawler(PythonAppCrawler):
    def cleanup_tree(self, tree):
        tree = super().cleanup_tree(tree)

        # Useless folder
        tree['children']['tmp'] = {
            'type': 'dir',
            'status': 'hidden'
        }
        tree['children']['wex.egg-info'] = {
            'type': 'dir',
            'status': 'hidden'
        }

        # Security tokens
        tree['children']['.env'] = {
            'type': 'file',
            'status': 'hidden'
        }

        return tree

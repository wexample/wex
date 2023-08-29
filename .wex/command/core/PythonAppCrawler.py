from core.AppCrawler import AppCrawler


class PythonAppCrawler(AppCrawler):
    def tree_remove(self, tree, file_name):
        keys_to_remove = []

        for key, value in tree.items():
            if key == file_name:
                keys_to_remove.append(key)
            elif isinstance(value, dict):
                self.tree_remove(value, file_name)

        for key in keys_to_remove:
            del tree[key]

    def cleanup_tree(self, tree):
        tree = super().cleanup_tree(tree)
        self.tree_remove(tree, '__pycache__')
        return tree

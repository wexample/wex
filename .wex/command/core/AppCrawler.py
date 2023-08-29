import os
import yaml


class AppCrawler:
    def __init__(self, root):
        self.root = root
        self.tree = {}

    def scan(self, root=None, tree=None):
        if root is None:
            root = self.root
        if tree is None:
            tree = self.tree

        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                if name not in tree:
                    tree[name] = {}
                self.scan(path, tree=tree[name])
            else:
                tree[name] = None

    def get_source_tree(self):
        tree = self.tree

        del tree['.git']
        tree['.wex']['tmp'] = {}

        return tree

    # Run all steps
    def build(self):
        self.scan()
        tree = self.get_source_tree()

        self.save_to_yaml('.wex/ai/data/tree.yml', tree)

    def save_to_yaml(self, filepath, tree):
        with open(filepath, 'w') as f:
            yaml.dump(tree, f, default_flow_style=False)

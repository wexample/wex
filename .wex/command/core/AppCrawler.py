import os
from datetime import datetime

import yaml


class AppCrawler:
    def __init__(self, root, yaml_filepath):
        self.root = root
        self.yaml_filepath = yaml_filepath

    def load_existing_yaml(self):
        try:
            with open(self.yaml_filepath, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}

    def merge_trees(self, old_tree, new_tree):
        for name, content in new_tree.items():
            if name not in old_tree:
                old_tree[name] = content
            elif "children" in old_tree[name]:
                self.merge_trees(old_tree[name]["children"], content["children"])

        # Remove deleted items
        for name in list(old_tree.keys()):
            if name not in new_tree:
                del old_tree[name]

    def scan(self, root=None, tree=None):
        if root is None:
            root = self.root
        if tree is None:
            tree = {}

        tree["description"] = ''
        tree["children"] = {}

        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                tree["children"][name] = {}
                self.scan(path, tree=tree["children"][name])
            else:
                tree["children"][name] = {
                    "description": ''
                }

        return tree

    def cleanup_tree(self, tree):
        # Do your specific removals here.
        del tree['children']['.git']
        tree['children']['.wex']['tmp'] = {}

        return tree

    def build(self):
        tree = self.load_existing_yaml()

        # Scan new files
        new_tree = self.cleanup_tree(
            self.scan()
        )

        # Merge with existing tree
        self.merge_trees(tree, new_tree)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tree['last_updated'] = timestamp
        self.save_to_yaml(self.yaml_filepath, tree)

    def save_to_yaml(self, filepath, tree):
        with open(filepath, 'w') as f:
            yaml.dump(tree, f, default_flow_style=False)

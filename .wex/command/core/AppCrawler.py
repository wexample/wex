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

    def merge_tree(self, old_tree: dict, new_tree: dict):
        merged_tree = old_tree.copy()

        if 'children' in new_tree:
            merged_tree['children'] = {}

            for name, children in new_tree['children'].items():
                if 'children' not in old_tree:
                    merged_tree['children'][name] = children.copy()
                else:
                    old_children = {}
                    if name in old_tree['children']:
                        old_children = old_tree['children'][name].copy()

                    merged_tree['children'][name] = self.merge_tree(
                        old_children,
                        children.copy()
                    )

        return merged_tree

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
        new_tree = self.merge_tree(tree, new_tree)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tree['last_updated'] = timestamp
        self.save_to_yaml(self.yaml_filepath, new_tree)

    def save_to_yaml(self, filepath, tree):
        with open(filepath, 'w') as f:
            yaml.dump(tree, f, default_flow_style=False)

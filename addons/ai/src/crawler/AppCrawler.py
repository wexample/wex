import os

from datetime import datetime
from typing import TypedDict, Optional

from src.const.types import YamlContentDict, StringKeysDict

import yaml


class CrawlerTreeItem(TypedDict, total=False):
    description: Optional[str]
    status: Optional[str]
    children: Optional[StringKeysDict]


class AppCrawler:
    def __init__(self, root: str, yaml_filepath: str) -> None:
        self.root: str = root
        self.yaml_filepath: str = yaml_filepath

    def load_tree(self) -> YamlContentDict:
        try:
            with open(self.yaml_filepath, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}

    def merge_tree(self, old_tree: dict, new_tree: dict) -> CrawlerTreeItem:
        merged_tree: CrawlerTreeItem = new_tree.copy()

        if 'description' in old_tree:
            merged_tree['description'] = old_tree['description']

        if 'status' in old_tree and old_tree["status"] == "hidden":
            merged_tree['status'] = "hidden"

            if "children" in merged_tree:
                del merged_tree["children"]
        else:
            if 'children' in new_tree:
                merged_tree['children'] = {}

                for name, children in new_tree['children'].items():
                    if isinstance(children, dict):
                        children = children.copy()

                    if 'children' not in old_tree:
                        merged_tree['children'][name] = children
                    else:
                        if name in old_tree['children']:
                            old_children = old_tree['children'][name]

                            if isinstance(old_children, dict):
                                old_children = old_children.copy()

                                merged_tree['children'][name] = self.merge_tree(
                                    old_children,
                                    children
                                )
                            else:
                                merged_tree['children'][name] = children
                        else:
                            merged_tree['children'][name] = children

        return merged_tree

    def scan(self, root=None, tree=None):
        if root is None:
            root = self.root
        if tree is None:
            tree = {}

        tree["children"] = {}

        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                tree["children"][name] = {
                    'type': 'dir'
                }
                self.scan(path, tree=tree["children"][name])
            else:
                tree["children"][name] = {
                    'type': 'file'
                }

        return tree

    def cleanup_tree(self, tree: CrawlerTreeItem) -> CrawlerTreeItem:
        tree['children']['.wex']['children']['ai']['children']['data']['children']['tree.yml'] = {
            'type': 'file',
            'status': 'hidden',
            'description': 'This current file'
        }

        tree['children']['.git'] = {
            'type': 'dir',
            'status': 'hidden'
        }

        tree['children']['.wex']['tmp'] = {
            'type': 'dir',
            'status': 'hidden'
        }

        return tree

    def build(self) -> list:
        tree = self.load_tree()

        # Scan new files
        new_tree = self.cleanup_tree(
            self.scan()
        )

        # Merge with existing tree
        new_tree = self.merge_tree(tree, new_tree)

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tree['last_updated'] = timestamp
        self.save_to_yaml(self.yaml_filepath, new_tree)

        return new_tree

    def save_to_yaml(self, filepath: str, tree: CrawlerTreeItem) -> None:
        with open(filepath, 'w') as f:
            yaml.dump(tree, f, default_flow_style=False)


import os
from datetime import datetime
from typing import Optional, TypedDict, cast

import yaml

from addons.app.const.app import APP_DIR_APP_DATA_NAME
from src.const.types import StringKeysDict
from wexample_helpers.helpers.dict import dict_merge


class CrawlerTreeItem(TypedDict, total=False):
    children: Optional[StringKeysDict]
    description: Optional[str]
    last_updated: Optional[str]
    status: Optional[str]


class AppCrawler:
    def __init__(self, root: str, yaml_filepath: str) -> None:
        self.root: str = root
        self.yaml_filepath: str = yaml_filepath

    def load_tree(self) -> CrawlerTreeItem:
        try:
            with open(self.yaml_filepath, "r") as f:
                return cast(CrawlerTreeItem, yaml.safe_load(f) or {})
        except FileNotFoundError:
            return cast(CrawlerTreeItem, {})

    def merge_tree(
        self, old_tree: CrawlerTreeItem, new_tree: CrawlerTreeItem
    ) -> CrawlerTreeItem:
        merged_tree: CrawlerTreeItem = new_tree.copy()

        if "description" in old_tree:
            merged_tree["description"] = old_tree["description"]

        if "status" in old_tree and old_tree["status"] == "hidden":
            merged_tree["status"] = "hidden"

            if "children" in merged_tree:
                del merged_tree["children"]
        else:
            if "children" in new_tree and new_tree["children"]:
                children: StringKeysDict = {}

                for name, child in new_tree["children"].items():
                    if isinstance(child, dict):
                        child = child.copy()

                    if "children" not in old_tree or not old_tree["children"]:
                        children[name] = child
                    else:
                        if name in old_tree["children"]:
                            old_child = cast(
                                CrawlerTreeItem, old_tree["children"][name]
                            )

                            if isinstance(old_child, dict):
                                old_child = old_child.copy()
                                children[name] = self.merge_tree(old_child, child)
                            else:
                                children[name] = child
                        else:
                            children[name] = child

                merged_tree["children"] = children

        return merged_tree

    def scan(
        self, root: Optional[str] = None, tree: Optional[CrawlerTreeItem] = None
    ) -> CrawlerTreeItem:
        if root is None:
            root = self.root
        if tree is None:
            tree = {}

        children: StringKeysDict = {}

        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                children[name] = {"type": "dir"}
                self.scan(path, tree=children[name])
            else:
                children[name] = {"type": "file"}

        tree["children"] = children

        return tree

    def cleanup_tree(self, tree: CrawlerTreeItem) -> CrawlerTreeItem:
        tree["children"] = dict_merge(
            tree["children"] or {},
            {
                ".git": {"type": "dir", "status": "hidden"},
                APP_DIR_APP_DATA_NAME: {
                    "children": {
                        "ai": {
                            "children": {
                                "data": {
                                    "children": {
                                        "tree.yml": {
                                            "type": "file",
                                            "status": "hidden",
                                            "description": "This current file",
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "tmp": {
                        "type": "dir",
                        "status": "hidden",
                    },
                },
            },
        )

        return tree

    def build(self) -> CrawlerTreeItem:
        tree = self.load_tree()

        # Scan new files
        new_tree = self.cleanup_tree(self.scan())

        # Merge with existing tree
        new_tree = self.merge_tree(tree, new_tree)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree["last_updated"] = timestamp
        self.save_to_yaml(self.yaml_filepath, new_tree)

        return new_tree

    def save_to_yaml(self, filepath: str, tree: CrawlerTreeItem) -> None:
        with open(filepath, "w") as f:
            yaml.dump(tree, f, default_flow_style=False)

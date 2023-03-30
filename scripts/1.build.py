import os
import datetime
import sys
import argparse
import re

def create_changelog(name, version, updates, owner, history):
    template = """{} ({}-1) unstable; urgency=low

{}

 -- {}  {}

{}

"""
    formatted_updates = "\n".join(f"  * {update}" for update in updates)
    date = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    changelog = template.format(name, version, formatted_updates, owner, date, history)

    return changelog

def get_latest_build(build_folder, build_limit):
    builds = []
    items = os.listdir(build_folder)

    sorted(items)
    for file in items:
        if file == build_limit:
            return builds[-1]
        builds.append(file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', type=str)
    parser.add_argument('-n', type=str)
    args = parser.parse_args()

    version = args.v
    name = args.n
    build_name = f'{name}_{version}'

    last_version = get_latest_build('.', build_name)
    last_changelog_path = f'{last_version}/debian/changelog'
    history = ''
    owner = 'wexample <contact@wexample.com>'
    if os.path.exists(last_changelog_path):
        with open(last_changelog_path) as f:
            history = f.read()

    updates = [
        'Automated deployment',
        'Something else'
    ]

    new_changelog = create_changelog(
      name,
      version,
      updates,
      owner,
      history
    )

    with open(f'{build_name}/debian/changelog', "w") as f:
        f.write(new_changelog)

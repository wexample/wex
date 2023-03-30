import os
import datetime
import argparse


class BuildManager:
    name: str = None
    version: str = None
    build_name: str = None
    owner: str = 'wexample <contact@wexample.com>'
    path: dict = {
        'root': None,
        'addons': None
    }

    def __init__(self, entrypoint_path):
        self.path['root'] = os.path.dirname(
            os.path.dirname(
                os.path.realpath(entrypoint_path)
            )
        ) + '/'
        self.path['templates'] = self.path['root'] + 'templates/'

        steps = [
            self.step_init_vars,
            self.step_build_changelog,
        ]

        for step in steps:
            print('Build step ' + step.__name__)
            step()

    def step_init_vars(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', type=str)
        parser.add_argument('-n', type=str)
        args = parser.parse_args()

        self.version = args.v
        self.name = args.n
        self.build_name = f'{self.name}_{self.version}'

    def get_latest_build(self, build_folder):
        builds = []
        items = os.listdir(build_folder)

        sorted(items)
        for file in items:
            if file == self.build_name:
                return builds[-1]
            builds.append(file)

        return None

    def step_build_changelog(self):
        last_version = self.get_latest_build('.')
        last_changelog_path = f'{last_version}/debian/changelog'
        history = ''

        if os.path.exists(last_changelog_path):
            with open(last_changelog_path) as f:
                history = f.read()

        updates = [
            'Automated deployment',
            'Something else'
        ]

        template = open(self.path['templates'] + 'changelog.tpl').read()
        formatted_updates = "\n".join(f"  * {update}" for update in updates)

        changelog = template.format(
            self.name,
            self.version,
            formatted_updates,
            self.owner,
            datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000'),
            history
        )

        with open(f'{self.build_name}/debian/changelog', "w") as f:
            f.write(changelog)

    def build_path(self, relative_path: str) -> str:
        return self.path['root'] + relative_path


if __name__ == "__main__":
    BuildManager(__file__)

import os
import datetime
import argparse
import shutil
import subprocess
import tarfile
import grp
import pwd
import urllib.request
import urllib.parse


class BuildManager:
    name: str = None
    version: str = None
    build_name: str = None
    owner: str = 'wexample <contact@wexample.com>'
    path: dict = {
        'root': None,
        'addons': None
    }
    gitlab_ci_api_v4_url = 'gitlab.wexample.com/api/v4'
    ci_project_id = None
    private_token = None

    def __init__(self, entrypoint_path):
        self.path['current'] = os.path.dirname(
            os.path.realpath(entrypoint_path)
        )
        self.path['root'] = os.path.dirname(self.path['current']) + '/'
        self.path['builds'] = self.path['root'] + 'builds/'
        self.path['templates'] = self.path['root'] + 'templates/'

        steps = [
            self.step_init_vars,
            self.step_cleanup_old_build,
            self.step_clone_source,
            self.step_cleanup_source,
            self.step_create_tarball,
            self.step_copy_debian,
            self.step_build_changelog,
            self.step_set_permissions,
            self.step_debuild,
            self.step_post_package,
        ]

        for step in steps:
            print('Build step ' + step.__name__)
            step()

        print('Done.')

    def step_init_vars(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v', type=str)
        parser.add_argument('-n', type=str)
        parser.add_argument('-gid', type=int)
        parser.add_argument('-gtk', type=str)
        args = parser.parse_args()

        self.version = args.v
        self.name = args.n
        self.ci_project_id = args.gid
        self.private_token = args.gtk
        self.build_name = f'{self.name}_{self.version}'

        self.path['build'] = self.path['builds'] + f'{self.build_name}/'
        self.path['build_source'] = self.path['build'] + self.name + '/'
        self.path['tarball'] = self.path['builds'] + self.build_name + '.orig.tar.gz'

    def step_cleanup_old_build(self):
        self.change_owner_recursive_current(self.path['build'])

        self.delete_dir(self.path['build'])
        self.delete_file(self.path['tarball'])
        os.mkdir(self.path['build'])

    def step_clone_source(self):
        subprocess.run([
            'git',
            'clone',
            self.path['root'] + 'source',
            self.path['build_source']
        ])

    def step_cleanup_source(self):
        self.delete_dir(self.path['build_source'] + '.git')
        self.delete_dir(self.path['build_source'] + '.wex')
        self.delete_file_recursive('.gitignore', self.path['build_source'])

    def step_create_tarball(self):
        with tarfile.open(self.path['tarball'], 'w:gz') as tar:
            tar.add(self.path['build'] + '/wex')

        self.change_owner_recursive_current(self.path['build'])

    def change_owner_recursive_current(self, path):
        if os.path.exists(path):
            owner_uid = pwd.getpwnam('owner').pw_uid
            owner_gid = grp.getgrnam('owner').gr_gid
            self.change_owner_recursive(path, owner_uid, owner_gid)

    def step_copy_debian(self):
        shutil.copytree(
            self.path['templates'] + 'debian', self.path['build'] + 'debian'
        )

        print(self.path['templates'] + 'debian')
        print(self.path['build'] + 'debian')

        shutil.copy(
            self.path['templates'] + 'wex.1', self.path['build']
        )

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

        with open(f'{self.path["build"]}/debian/changelog', "w") as f:
            f.write(changelog)

    def step_set_permissions(self):
        self.change_owner_recursive_current(self.path['build'])

        # Execution permission for cli only
        subprocess.run(['chmod', '-R', '-x', self.path['build_source']])
        subprocess.run(['chmod', '-R', '+x', self.path['build_source'] + 'cli'])

        # Execution permission for .sh files
        subprocess.run([
            'find',
            self.path['build_source'],
            '-name',
            '*.sh',
            '-type',
            'f',
            '-exec',
            'chmod',
            '+x',
            '{}',
            ';'
        ])

        # All "folders" have 755 permission
        subprocess.run([
            'find',
            self.path['build_source'],
            '-type',
            'd',
            '-exec',
            'chmod',
            '755',
            '{}',
            ';'
        ])

    def step_debuild(self):
        os.chdir(self.path['build'])

        subprocess.run([
            'debuild',
            '-us',
            '-uc',
        ])

        os.chdir(self.path['current'])

    def step_post_package(self):
        deb_file_path = self.build_name + '-1_all.deb'
        # Tilde is not supported
        version = self.version.replace('~', '-')
        package_name = self.build_name.replace('~', '-') + '.deb'

        url = f"https://{self.gitlab_ci_api_v4_url}/projects/{self.ci_project_id}/packages/generic/wex/{version}/{package_name}"
        headers = {'PRIVATE-TOKEN': self.private_token}

        with open(self.path['builds'] + deb_file_path, 'rb') as f:
            data = f.read()
            req = urllib.request.Request(url, data=data, headers=headers, method='PUT')

        with urllib.request.urlopen(req) as response:
            print(response.read().decode('utf-8'))

    def get_latest_build(self, build_folder):
        builds = []
        items = os.listdir(build_folder)

        sorted(items)
        for file in items:
            if file == self.build_name:
                return builds[-1]
            builds.append(file)

        return None

    def change_owner_recursive(self, path, owner_uid, owner_gid):
        for dir_path, dir_names, filenames in os.walk(path):
            shutil.chown(dir_path, owner_uid, owner_gid)
            for filename in filenames:
                filepath = os.path.join(dir_path, filename)
                if os.path.islink(filepath):
                    os.lchown(filepath, owner_uid, owner_gid)
                else:
                    shutil.chown(filepath, owner_uid, owner_gid)

    def delete_file_recursive(self, file_name, start_path):
        for root, _, files in os.walk(start_path):
            for file in files:
                if file == file_name:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

    def delete_file(self, path):
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)

    def delete_dir(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            shutil.rmtree(path)


if __name__ == "__main__":
    BuildManager(__file__)

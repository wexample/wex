from typing import Optional

import click
import git
from addons.default.command.version.increment import default__version__increment
from addons.app.command.config.get import app__config__get
from addons.app.command.config.set import app__config__set
from src.const.error import ERR_UNEXPECTED


@click.command
@click.pass_obj
@click.option('--version', '-v', type=str, required=False,
              help="New version number, auto generated if missing")
@click.option('--commit', '-ok', required=False, is_flag=True, default=False,
              help="New version changes has been validated, ask to commit changes")
@click.option('--app-dir', '-a', type=str, required=True,
              help="App directory")
def app__version__build(kernel, version=None, commit: bool = False, app_dir: Optional[str] = False):
    if not commit:
        if version:
            new_version = version
        else:
            new_version = kernel.exec_function(
                default__version__increment,
                {
                    'version': kernel.exec_function(
                        app__config__get,
                        {
                            'key': 'global.version'
                        }
                    )
                }
            )

        # Save new version
        kernel.log(f'New app version : {new_version}')
        kernel.exec_function(
            app__config__set,
            {
                'key': 'global.version',
                'value': new_version
            }
        )
    else:
        repo = git.Repo(app_dir)
        new_version = kernel.exec_function(
            app__config__get,
            {
                'key': 'global.version'
            }
        )

        if not repo.is_dirty(untracked_files=True):
            kernel.log('No changes to commit')
            return

        kernel.log('Updating repo...')
        try:
            origin = repo.remote(name='origin')
            origin.fetch(tags=True)
            origin.pull()
        except Exception as e:
            kernel.error(ERR_UNEXPECTED, {
                'error': 'Git pull : ' + str(e),
            })

        # Get the last tag.
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        latest_tag = tags[-1]

        if str(latest_tag) == new_version:
            kernel.error(ERR_UNEXPECTED, {
                'error': f'The version {new_version} has been already tagged, you should create a new version.',
            })

        kernel.log('Committing new version...')
        try:
            repo.index.add('.wex/config')
            repo.index.commit(f"New version v{new_version}")
            repo.create_tag(f'{new_version}')

            # origin.push()
        except Exception as e:
            kernel.error(ERR_UNEXPECTED, {
                'error': 'Git commit : ' + str(e),
            })

        kernel.message(f'New version : {new_version}')

    return new_version

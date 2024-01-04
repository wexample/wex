from src.helper.command import execute_command_sync
from addons.app.command.remote.push import app__remote__push
from addons.app.tests.AbstractAppTestCase import AbstractAppTestCase
from addons.app.command.remote.exec import app__remote__exec


class TestAppCommandRemotePush(AbstractAppTestCase):
    def test_push(self) -> None:
        self.start_remote_server()

        manager = self.create_and_start_test_app_with_remote(services=["php"])
        app_dir = manager.get_app_dir()
        test_filename = "structure-test.txt"

        manager.set_config("structure", {
            test_filename: {
                "type": "file",
                "should_exist": True,
                "on_missing": "create",
                "default_content": "This is a test file created by structure manager",
                "remote": "push"
            },
        })

        # Reload updated config
        manager._directory.initialize()
        environment = "test-remote"

        execute_command_sync(
            manager.kernel,
            ["touch", f"{app_dir}test.txt"])

        self.kernel.run_function(
            app__remote__push, {
                "environment": "test-remote",
                "app-dir": app_dir
            }
        )

        remote_path = f"/var/www/{environment}/{manager.get_config('global.name').get_str()}/"

        response = manager.kernel.run_function(
            app__remote__exec,
            {
                "app-dir": app_dir,
                "environment": environment,
                "command": f"ls -la {remote_path}{test_filename}"
            }
        )

        self.assertTrue(
            response.first().startswith('-rw'),
            "The local file has been created remotely"
        )

        self.stop_remote_server()


        # # TODO On modifie le fonctionnement attach.before / after pour permettre a mysql d'exécuter un fonction before remote/push (pour faire un dump) et after remote/pull (pour monter le dernier dump)
        # # TODO Lors de l'install (+migration), mysql ajoute le dossier mysql/dumps (ou bien le dernier dump uniquement)
        # # TODO On crée remote/pull qui est un webhook provoquant un push
        # # TODO On créee une manière de faire un webhook et d'attendre qu'il se termine avant de continuer, pour le CI/CD
        # # TODO On ajoute cette synchro a TPA de prod > dev (synchro manuelle)
        # # TODO On permets au CI/CD de copier le site de dev (ou en partie) pour réaliser les tests
        # # TODO On passe les tests sur le site de dev
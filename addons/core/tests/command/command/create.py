from tests.AbstractTestCase import AbstractTestCase
import os
import shutil


class TestCoreCommandCommandCreate(AbstractTestCase):
    def test_create(self):
        scripts = self.kernel.exec('core::command/create', {
            'command': 'core::some/thing'
        })

        for file_path in [scripts['command'], scripts['test']]:
            self.assertFileExists(file_path)

            self.kernel.log(f'Removing file : {file_path}')

            os.remove(file_path)

            shutil.rmtree(
                os.path.dirname(file_path)
            )

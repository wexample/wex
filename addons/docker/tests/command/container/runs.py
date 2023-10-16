from addons.docker.command.container.runs import docker__container__runs
from tests.AbstractTestCase import AbstractTestCase


class TestDockerCommandContainerRuns(AbstractTestCase):
    def test_runs(self):
        response = self.kernel.run_function(
            docker__container__runs,
            {
                'name': 'lorem_ipsum'
            })

        self.assertFalse(response.first())

        self.start_docker_container('test_container_runs')

        response = self.kernel.run_function(
            docker__container__runs,
            {
                'name': 'test_container_runs'
            })

        self.assertTrue(response.first())

        self.remove_docker_container('test_container_runs')

import os
import unittest


class TestManager:
    kernel = None

    def __init__(self, kernel):
        self.kernel = kernel

    def call(self, command):
        self.kernel.log('Starting test suite..')

        loader = unittest.TestLoader()
        suite = loader.discover(self.kernel.path['root'] + 'tests/')

        os.chdir(self.kernel.path['root'])

        unittest.TextTestRunner().run(suite)

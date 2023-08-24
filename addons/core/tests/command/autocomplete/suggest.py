import os.path
import time

from addons.core.command.autocomplete.suggest import core__autocomplete__suggest
from addons.core.command.command.create import core__command__create
from src.const.globals import COMMAND_CHAR_USER, COMMAND_CHAR_SERVICE, COMMAND_CHAR_APP, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandAutocompleteSuggest(AbstractTestCase):
    def test_suggest(self):
        # User ask "", it should suggest all
        # addons names suffixed by "::",
        # and every special char namespaces : ~, ., @
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 0,
                'search': ''
            }
        )

        self.assertTrue(COMMAND_CHAR_APP in suggestions)
        self.assertTrue(COMMAND_CHAR_SERVICE in suggestions)
        # Do not test user char as it may not exist at this point

        # User ask "co", it should suggest "core::",
        # with addon separator as there is no more
        # addon name starting with "co"
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 0,
                'search': 'co'
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 1
        )

        # User ask "core:", it should suggest "core::"
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 1,
                'search': ' '.join(['core', ':'])
            }
        )

        self.assertTrue(
            suggestions == ':'
        )

        # User ask "core::", it should suggest all groups in core::*
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 1,
                'search': ' '.join(['core', COMMAND_SEPARATOR_ADDON])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 2
        )

        # User ask "core::co", it should suggest all groups in core::co*
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 2,
                'search': ' '.join([
                    'core',
                    COMMAND_SEPARATOR_ADDON,
                    'co'
                ])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 2
        )

        # User ask "core::logo", it should suggest single result core::logo/show
        # It may fail in the future if we add a new logo/xx command
        # We'll found another command in this case
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 2,
                'search': ' '.join([
                    'core',
                    COMMAND_SEPARATOR_ADDON,
                    'logo'
                ])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) == 1
        )

        # User ask "core::logo/show",
        # it suggests only the found command
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 2,
                'search': ' '.join([
                    'core',
                    COMMAND_SEPARATOR_ADDON,
                    'logo',
                    COMMAND_SEPARATOR_GROUP,
                    'show'
                ])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) == 1
        )

    def tests_suggest_addon_args(self):
        # Search full addon command name with a final space
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 3,
                'search': ' '.join([
                    'core',
                    COMMAND_SEPARATOR_ADDON,
                    'autocomplete' + COMMAND_SEPARATOR_GROUP + 'suggest'
                ])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 2
        )

    def tests_suggest_service(self):
        # Search only "@", should return all service commands
        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 0,
                'search': COMMAND_CHAR_SERVICE
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 2
        )

        self.assertTrue(
            COMMAND_CHAR_SERVICE + 'test::demo-command' in suggestions
        )

        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 1,
                'search': COMMAND_CHAR_SERVICE + ' t'
            }
        )

        self.assertTrue(
            COMMAND_CHAR_SERVICE + 'test::demo-command' in suggestions
        )

        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 2,
                'search': ' '.join(
                    [
                        COMMAND_CHAR_SERVICE,
                        'test',
                        ':'
                    ]
                )
            }
        )

        # It should be only one suggestion for test-2
        self.assertEqual(
            suggestions,
            ':'
        )

        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 2,
                'search': ' '.join(
                    [
                        COMMAND_CHAR_SERVICE,
                        'test-2',
                        COMMAND_SEPARATOR_ADDON
                    ]
                )
            }
        )

        # It should be only one suggestion for test-2
        self.assertEqual(
            suggestions,
            'another-demo-command/test'
        )

    def tests_suggest_service_args(self):
        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 4,
                'search': ' '.join(
                    [
                        COMMAND_CHAR_SERVICE,
                        'test',
                        COMMAND_SEPARATOR_ADDON,
                        'demo-command' + COMMAND_SEPARATOR_GROUP + 'first',
                    ]
                ) + ' '
            }
        )

        self.assertTrue(
            '--option' in suggestions
        )

    def create_and_test_created_command(self, prefix: str, search: str = None):
        command = prefix + 'test/autocomplete_command'
        if not search:
            search = prefix + 'te'

        self.kernel.log(f'Testing command {command}')

        # First create command
        info = self.kernel.exec_function(
            core__command__create,
            {
                'command': command
            }
        )

        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 0,
                'search': search
            }
        )

        self.assertTrue(
            command in suggestions,
            f'Suggestions "{suggestions}" contains "{command}"'
        )

        self.assertTrue(
            os.path.isfile(
                info['command']
            )
        )

        os.remove(info['command'])

        # Test is optional at this point
        if info['test']:
            os.remove(info['test'])

    def tests_suggest_app(self):
        # Search only ".", should return all app commands
        suggestions: str = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 0,
                'search': COMMAND_CHAR_APP
            }
        )

        # There is at least on custom app command in wex
        self.assertTrue(
            len(suggestions.split(' ')) >= 1
        )

        # Search ".te", to find created command
        self.create_and_test_created_command(
            COMMAND_CHAR_APP,
        )

    def tests_suggest_app_args(self):
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 1,
                'search': COMMAND_CHAR_APP + 'local_command' + COMMAND_SEPARATOR_GROUP + 'test '
            }
        )

        self.assertTrue(
            'local-option' in suggestions
        )

    def tests_suggest_user(self):
        # Search "~te", to find created command
        self.create_and_test_created_command(
            COMMAND_CHAR_USER,
        )

    def tests_suggest_user_args(self):
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 1,
                'search': COMMAND_CHAR_USER + 'undefined/command '
            }
        )

        # User command may not exist during test,
        # we just check if undefined command completion does not fail.
        self.assertEqual(
            suggestions,
            ''
        )

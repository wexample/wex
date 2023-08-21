from addons.core.command.autocomplete.suggest import core__autocomplete__suggest
from src.const.globals import COMMAND_CHAR_USER, COMMAND_CHAR_SERVICE, COMMAND_CHAR_APP, COMMAND_SEPARATOR_ADDON, \
    COMMAND_SEPARATOR_GROUP
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandAutocompleteSuggest(AbstractTestCase):
    def test_suggest(self):
        self.check_suggest_addon()
        self.check_suggest_addon_args()

    def check_suggest_addon(self):
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
        self.assertTrue(COMMAND_CHAR_USER in suggestions)

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

    def check_suggest_addon_args(self):
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': 3,
                'search': ' '.join([
                    'core',
                    COMMAND_SEPARATOR_ADDON,
                    'autocomplete' + COMMAND_SEPARATOR_GROUP + 'suggest'
                    ' '
                ])
            }
        )

        self.assertTrue(
            len(suggestions.split(' ')) >= 2
        )

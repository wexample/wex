from addons.core.command.autocomplete.suggest import core__autocomplete__suggest
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandAutocompleteSuggest(AbstractTestCase):
    def check_suggestion_command(self, cursor, should_success=True):
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': cursor,
                'search': '  '.join([
                    'app',
                    '::',
                    'config/set',
                ])
            }
        )

        self.kernel.log(f'Autocomplete suggestion (cursor {cursor}) : "{suggestions}"')

        if should_success:
            self.assertTrue(bool(suggestions.strip()))
        else:
            self.assertEqual(suggestions, '')

    def check_suggestion_service(self, cursor, should_success=True):
        suggestions = self.kernel.exec_function(
            core__autocomplete__suggest,
            {
                'cursor': cursor,
                'search': '  '.join([
                    '@proxy',
                    'started',
                ])
            }
        )

        self.kernel.log(f'Autocomplete suggestion (cursor {cursor}) : "{suggestions}"')

    def test_suggest(self):
        self.check_suggest_addon()
        self.check_suggest_service()

    def check_suggest_addon(self):
        self.check_suggestion_command(0)
        self.check_suggestion_command(1)
        self.check_suggestion_command(2)
        self.check_suggestion_command(3, False)
        self.check_suggestion_command(4, False)

    def check_suggest_service(self):
        self.check_suggestion_service(0)

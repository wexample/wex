from addons.core.command.autocomplete.suggest import core__autocomplete__suggest
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandAutocompleteSuggest(AbstractTestCase):
    def check_suggestion(self, cursor, should_success=True):
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

        self.kernel.log(f'Autocomplete suggestion : "{suggestions}"')

        if should_success:
            self.assertTrue(bool(suggestions.strip()))
        else:
            self.assertEqual(suggestions, '')

    def test_suggest(self):
        self.check_suggestion(0)
        self.check_suggestion(1)
        self.check_suggestion(2)
        self.check_suggestion(3, False)

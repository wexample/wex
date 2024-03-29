import os.path
from typing import Optional

from addons.app.AppAddonManager import AppAddonManager
from addons.app.helper.test import DEFAULT_APP_TEST_NAME, test_create_app
from addons.core.command.autocomplete.suggest import core__autocomplete__suggest
from addons.core.command.command.create import core__command__create
from src.const.globals import (
    COMMAND_CHAR_APP,
    COMMAND_CHAR_SERVICE,
    COMMAND_CHAR_USER,
    COMMAND_SEPARATOR_ADDON,
    COMMAND_SEPARATOR_GROUP,
)
from tests.AbstractTestCase import AbstractTestCase


class TestCoreCommandAutocompleteSuggest(AbstractTestCase):
    def test_suggest(self) -> None:
        # User ask "", it should suggest all
        # addons names suffixed by "::",
        # and every special char namespaces : ~, ., @
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest, {"cursor": 0, "search": ""}
        ).first()

        self.assertTrue(COMMAND_CHAR_APP in suggestions)
        self.assertTrue(COMMAND_CHAR_SERVICE in suggestions)
        # Do not test user char as it may not exist at this point

        # User ask "co", it should suggest "core::",
        # with addon separator as there is no more
        # addon name starting with "co"
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest, {"cursor": 0, "search": "co"}
        ).first()

        self.assertTrue(len(suggestions.split(" ")) >= 1)

        # User ask "core:", it should suggest "core::"
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 1, "search": " ".join(["core", ":"])},
        ).first()

        self.assertTrue(suggestions == ":")

        # User ask "core::", it should suggest all groups in core::*
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 1, "search": " ".join(["core", COMMAND_SEPARATOR_ADDON])},
        ).first()

        self.assertTrue(len(suggestions.split(" ")) >= 2)

        # User ask "core::co", it should suggest all groups in core::co*
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 2, "search": " ".join(["core", COMMAND_SEPARATOR_ADDON, "co"])},
        ).first()

        self.assertTrue(len(suggestions.split(" ")) >= 2)

        # User ask "core::logo", it should suggest single result core::logo/show
        # It may fail in the future if we add a new logo/xx command
        # We'll found another command in this case
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 2,
                "search": " ".join(["core", COMMAND_SEPARATOR_ADDON, "logo"]),
            },
        ).first()

        self.assertTrue(len(suggestions.split(" ")) == 1)

        # User ask "core::logo/show",
        # it suggests only the found command
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 2,
                "search": " ".join(
                    [
                        "core",
                        COMMAND_SEPARATOR_ADDON,
                        "logo",
                        COMMAND_SEPARATOR_GROUP,
                        "show",
                    ]
                ),
            },
        ).first()

        self.assertTrue(len(suggestions.split(" ")) == 1)

    def tests_suggest_addon_args(self) -> None:
        # Search full addon command name with a final space
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 3,
                "search": " ".join(
                    [
                        "core",
                        COMMAND_SEPARATOR_ADDON,
                        "autocomplete" + COMMAND_SEPARATOR_GROUP + "suggest --s",
                    ]
                ),
            },
        ).first()

        self.assertTrue("--search" in suggestions)

    def tests_suggest_service(self) -> None:
        suggestions: str

        # Search only "@", should return all service commands
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest, {"cursor": 0, "search": COMMAND_CHAR_SERVICE}
        ).first()

        self.assertTrue(len(suggestions.split(" ")) >= 2)

        self.assertTrue(COMMAND_CHAR_SERVICE + "test::demo-command" in suggestions)

        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 1, "search": COMMAND_CHAR_SERVICE + " t"},
        ).first()

        self.assertTrue(COMMAND_CHAR_SERVICE + "test::demo-command" in suggestions)

        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 2, "search": " ".join([COMMAND_CHAR_SERVICE, "test", ":"])},
        ).first()

        # It should be only one suggestion for test-2
        self.assertEqual(suggestions, ":")

        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 2,
                "search": " ".join(
                    [COMMAND_CHAR_SERVICE, "test-2", COMMAND_SEPARATOR_ADDON]
                ),
            },
        ).first()

        # It should be only one suggestion for test-2
        self.assertEqual(suggestions, "another-demo-command/test")

    def tests_suggest_service_args(self) -> None:
        suggestions: str = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 4,
                "search": " ".join(
                    [
                        COMMAND_CHAR_SERVICE,
                        "test",
                        COMMAND_SEPARATOR_ADDON,
                        "demo-command" + COMMAND_SEPARATOR_GROUP + "first",
                    ]
                )
                + " ",
            },
        ).first()

        self.assertTrue("--option" in suggestions)

    def _create_and_test_created_command(
        self, prefix: str, search: Optional[str] = None
    ) -> None:
        command = prefix + "test/autocomplete-command"
        if not search:
            search = prefix + "te"

        self.log(f"Testing command {command}")

        # First create command
        info = self.kernel.run_function(
            core__command__create, {"command": command}
        ).first()

        suggestions: str = self.kernel.run_function(
            core__autocomplete__suggest, {"cursor": 0, "search": search}
        ).first()

        self.assertTrue(
            command in suggestions,
            f'Suggestions "{suggestions}" contains "{command}" when search for {search}',
        )

        self.assertTrue(os.path.isfile(info["command"]))

        os.remove(info["command"])

        # Test is optional at this point
        if info["test"]:
            os.remove(info["test"])

    def tests_suggest_app(self) -> None:
        app_dir = test_create_app(self.kernel, DEFAULT_APP_TEST_NAME)

        def _callback() -> None:
            # Search only ".", should return all app commands
            suggestions: str = self.kernel.run_function(
                core__autocomplete__suggest, {"cursor": 0, "search": COMMAND_CHAR_APP}
            ).first()

            # There is at least on custom app command in wex
            self.assertTrue(len(suggestions.split(" ")) >= 1)

            # Search ".te", to find created command
            self._create_and_test_created_command(
                COMMAND_CHAR_APP,
            )

        manager = self.kernel.addons["app"]
        assert isinstance(manager, AppAddonManager)

        manager.exec_in_app_workdir(app_dir, _callback)

    def tests_suggest_app_args(self) -> None:
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {
                "cursor": 1,
                "search": COMMAND_CHAR_APP
                + "local_command"
                + COMMAND_SEPARATOR_GROUP
                + "test ",
            },
        ).first()

        self.assertTrue("local-option" in suggestions)

    def tests_suggest_user(self) -> None:
        # Search "~te", to find created command
        self._create_and_test_created_command(
            COMMAND_CHAR_USER,
        )

    def tests_suggest_user_args(self) -> None:
        suggestions = self.kernel.run_function(
            core__autocomplete__suggest,
            {"cursor": 1, "search": COMMAND_CHAR_USER + "undefined/command "},
        ).first()

        # User command may not exist during test,
        # we just check if undefined command completion does not fail.
        self.assertEqual(suggestions, "")

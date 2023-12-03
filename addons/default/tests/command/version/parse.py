from addons.default.command.version.parse import default__version__parse
from addons.default.const.default import UPGRADE_TYPE_BETA
from tests.AbstractTestCase import AbstractTestCase


class TestDefaultCommandVersionParse(AbstractTestCase):
    def test_parse(self) -> None:
        test_cases = [
            (
                "5.0.0-beta.41+build.20230822134237",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": 0,
                    "pre_build_type": UPGRADE_TYPE_BETA,
                    "pre_build_number": 41,
                },
            ),
            (
                "5.0.0-beta.41+build.",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": 0,
                    "pre_build_type": UPGRADE_TYPE_BETA,
                    "pre_build_number": 41,
                },
            ),
            (
                "5.0.0-beta.41+",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": 0,
                    "pre_build_type": UPGRADE_TYPE_BETA,
                    "pre_build_number": 41,
                },
            ),
            (
                "5.0.0-beta.",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": 0,
                    "pre_build_type": UPGRADE_TYPE_BETA,
                    "pre_build_number": None,
                },
            ),
            (
                "5.0.0-",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": 0,
                    "pre_build_type": None,
                    "pre_build_number": None,
                },
            ),
            (
                "5.0.",
                {
                    "major": 5,
                    "intermediate": 0,
                    "minor": None,
                    "pre_build_number": None,
                },
            ),
            (
                "5.",
                {
                    "major": 5,
                    "intermediate": None,
                    "minor": None,
                    "pre_build_number": None,
                },
            ),
            (
                "lorem",
                {
                    "major": None,
                    "intermediate": None,
                    "minor": None,
                    "pre_build_number": None,
                },
            ),
        ]

        for version, expected in test_cases:
            self.log("Testing " + version)

            result = self.kernel.run_function(
                default__version__parse, {"version": version}
            ).first()
            assert isinstance(result, dict)
            assert isinstance(expected, dict)

            self.assertDictKeysEquals(result, expected)

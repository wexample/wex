import re
from typing import TYPE_CHECKING, Dict, Optional

from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Parse a version string and return its components")
@option("--version", "-v", type=str, required=True, help="The version string to parse")
def default__version__parse(
    kernel: "Kernel", version: str
) -> Dict[str, Optional[str]] | None:
    pre_build_number: Optional[int] = None
    pre_build_type: Optional[str] = None

    try:
        # Handle 1.0.0-beta.1+build.1234
        if "-" in version:
            base_version, pre_build = version.split("-")

            if "." in pre_build:
                pre_build_parts = pre_build.split(".")
                if len(pre_build_parts) == 2:
                    pre_build_type, pre_build_number = pre_build_parts
                else:
                    pre_build_type, pre_build_number, _ = pre_build_parts

                # pre_build_number can be : 1+build.1234
                if "+" in pre_build_number:
                    pre_build_number, build_metadata = pre_build_number.split("+")

                pre_build_number = int(pre_build_number) if pre_build_number else None

        match = re.match(r"(\d+)?\.?(\d+)?\.?(\d+)?([-.+].*)?", version)
        major = intermediate = minor = None

        if match:
            major, intermediate, minor, _ = match.groups()

        # Create a dictionary to store the elements
        version_dict = {
            "major": int(major) if major else None,
            "intermediate": int(intermediate) if intermediate else None,
            "minor": int(minor) if minor else None,
            "pre_build_type": pre_build_type,
            "pre_build_number": pre_build_number,
        }
    except Exception:
        return None

    return version_dict

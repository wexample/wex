import re
from typing import TYPE_CHECKING, Optional

from src.const.typing import VersionDescriptor
from src.decorator.command import command
from src.decorator.option import option

if TYPE_CHECKING:
    from src.core.Kernel import Kernel


@command(help="Parse a version string and return its components")
@option("--version", "-v", type=str, required=True, help="The version string to parse")
def default__version__parse(kernel: "Kernel", version: str) -> VersionDescriptor | None:
    pre_build_number: Optional[int] = None
    pre_build_type: Optional[str] = None

    try:
        # Handle 1.0.0-beta.1+build.1234
        if "-" in version:
            base_version, pre_build = version.split("-")

            if "." in pre_build:
                pre_build_parts = pre_build.split(".")
                pre_build_type = pre_build_parts[0]

                # pre_build_number can be : 1+build.1234
                if "+" in pre_build_parts[1]:
                    pre_build_number_str, build_metadata = pre_build_parts[1].split("+")
                    pre_build_number = (
                        int(pre_build_number_str) if pre_build_number_str else None
                    )
                else:
                    pre_build_number = (
                        int(pre_build_parts[1]) if pre_build_parts[1] else None
                    )

        match = re.match(r"(\d+)?\.?(\d+)?\.?(\d+)?([-.+].*)?", version)
        major = intermediate = minor = None

        if match:
            major, intermediate, minor, _ = match.groups()

        # Create a dictionary to store the elements
        version_dict: VersionDescriptor = {
            "major": int(major) if major else None,
            "intermediate": int(intermediate) if intermediate else None,
            "minor": int(minor) if minor else None,
            "pre_build_type": pre_build_type,
            "pre_build_number": pre_build_number,
        }
    except Exception:
        return None

    return version_dict

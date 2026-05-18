"""Poll PyPI until every wexample-* version pinned in requirements.txt is visible.

Intended to run as an intermediate CI step between `deploy` and the
`checkup_install_*` jobs: when a freshly published version hasn't yet propagated
to the CDN edge hit by the install jobs, those fail with "No matching
distribution found". This script blocks until `pip index versions` (which
mirrors what `pip install` does) sees every pinned wexample version.

Only wexample-* packages are checked — third-party deps are always already
propagated and would just slow us down.

Usage:
    python ci/wait_for_pypi_versions.py [requirements.txt]
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

_TIMEOUT_SECONDS = 30 * 60  # 30 min total
_POLL_INTERVAL_SECONDS = 30
_PIP_INDEX_TIMEOUT_SECONDS = 30
_PACKAGE_PREFIX = "wexample-"

_PIN_RE = re.compile(r"^([A-Za-z0-9._-]+)==([A-Za-z0-9._+-]+)\s*$")


def parse_pins(requirements_path: Path) -> list[tuple[str, str]]:
    """Return [(package, version), ...] for wexample-* pins in the file."""
    pins: list[tuple[str, str]] = []
    for raw_line in requirements_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _PIN_RE.match(line)
        if not match:
            continue
        package, version = match.group(1), match.group(2)
        if package.startswith(_PACKAGE_PREFIX):
            pins.append((package, version))
    return pins


def pip_sees_version(package: str, version: str) -> bool:
    """Return True if `pip index versions` reports the version as available."""
    try:
        result = subprocess.run(
            ["pip", "index", "versions", package],
            capture_output=True,
            text=True,
            timeout=_PIP_INDEX_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return False
    if result.returncode != 0:
        return False
    # `pip index versions` prints a comma-separated list on the "Available versions:" line.
    return version in {v.strip() for v in result.stdout.replace(",", " ").split()}


def main(argv: list[str]) -> int:
    requirements_path = Path(argv[1] if len(argv) > 1 else "requirements.txt")
    if not requirements_path.exists():
        print(f"requirements.txt not found: {requirements_path}", file=sys.stderr)
        return 2

    pins = parse_pins(requirements_path)
    if not pins:
        print(f"No {_PACKAGE_PREFIX}* pins in {requirements_path}; nothing to wait for.")
        return 0

    print(f"Waiting for {len(pins)} {_PACKAGE_PREFIX}* version(s) to appear on PyPI…")

    deadline = time.monotonic() + _TIMEOUT_SECONDS
    pending = list(pins)

    while pending:
        still_pending: list[tuple[str, str]] = []
        for package, version in pending:
            if pip_sees_version(package, version):
                print(f"  ✓ {package}=={version}")
            else:
                still_pending.append((package, version))
                print(f"  · {package}=={version} not yet visible")

        if not still_pending:
            print("All versions visible to pip; CDN propagation done.")
            return 0

        if time.monotonic() >= deadline:
            print(
                f"Timed out after {_TIMEOUT_SECONDS // 60} min waiting for: "
                + ", ".join(f"{p}=={v}" for p, v in still_pending),
                file=sys.stderr,
            )
            return 1

        pending = still_pending
        print(
            f"{len(pending)} version(s) still missing; retrying in "
            f"{_POLL_INTERVAL_SECONDS}s…"
        )
        time.sleep(_POLL_INTERVAL_SECONDS)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

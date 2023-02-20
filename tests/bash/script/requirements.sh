#!/usr/bin/env bash

scriptRequirementsTest() {
    _wexTestAssertNotEmpty "$(wex-exec script/requirements -s=file/convertLinesFormat)"

    _wexTestAssertEqual "$(wex-exec script/requirements -s=core/logo)" ""
}

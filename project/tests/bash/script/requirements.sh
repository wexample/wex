#!/usr/bin/env bash

scriptRequirementsTest() {
    _wexTestAssertNotEmpty "$(wex script/requirements -s=file/convertLinesFormat)"

    _wexTestAssertEqual "$(wex script/requirements -s=core/logo)" ""
}

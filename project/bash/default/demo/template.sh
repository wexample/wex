
demoTemplate() {
  local LONG_TEXT
  LONG_TEXT="with a long long long long text, allow to test screen with detection, and messages auto truncation"

  _wexTitle "This is a title"
  echo ""

  _wexLog "Simple log message..."
  _wexLog "Simple second log message..."
  _wexLog "Simple log message ${LONG_TEXT}"
  echo ""

  _wexSubTitle "This is a subtitle"
  echo ""

  _wexItem "one" "\t\tThis is list item"
  _wexItem "two" "\t\tThis is second list item"
  _wexItem "three" "\t\tThis is third list item"
  _wexItem "four" "\t\tThis is an item description ${LONG_TEXT}"
  _wexItem "This is a single sentence"
  _wexItem "This is a single sentence ${LONG_TEXT}"
  _wexItemSuccess success "\tCongratulations"
  _wexItemFail fail "\t\tOops"
  echo ""

  _wexMessage "This is a message" "With an extra information"
  echo ""

  _wexError "This is an error message" "With an extra information"
  echo ""
}
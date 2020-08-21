
demoTemplate() {
  _wexTitle "This is a title"
  echo ""

  _wexLog "Simple log message..."
  _wexLog "Simple second log message..."
  _wexLog "Simple log message with a long long long long text, allow to test screen with detection, and messages auto truncation"
  echo ""

  _wexSubTitle "This is a subtitle"
  echo ""

  _wexItem "one" "\t\tThis is list item"
  _wexItem "two" "\t\tThis is second list item"
  _wexItem "three" "\t\tThis is third list item"
  _wexItem "This is a single sentence"
  _wexItemSuccess success "\tCongratulations"
  _wexItemFail fail "\t\tOops"
  echo ""

  _wexMessage "This is a message" "With an extra information"
  echo ""

  _wexError "This is an error message" "With an extra information"
  echo ""
}
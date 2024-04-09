def patch_is_valid(text: str) -> bool:
    # Check hunt header
    if "@@" not in text:
        return False

    # Search for any + or - line
    lines = text.split("\n")
    for line in lines:
        if line.startswith("+") or line.startswith("-"):
            return True

    return False

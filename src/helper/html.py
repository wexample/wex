import re


def html_remove_tags(text):
    # Use a regular expression to find and remove tags
    # This regex matches anything that looks like HTML/XML tag and replaces it with an empty string
    return re.sub(r"<[^>]*>", "", text)


def html_split_prompt_parts(prompt_body: str) -> list[str]:
    parts = re.split(r"(<[^>]*>[^<]*<\/[^>]*>)", prompt_body)
    parts = [part for part in parts if part.strip()]
    result = []

    if not len(parts):
        return []

    temp = parts[0]
    for part in parts[1:]:
        if "<" in part and ">" in part:
            temp += part
        else:
            result.append(temp)
            temp = part
    result.append(temp)
    return result

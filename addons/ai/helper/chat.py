
TEXT_ALIGN_LEFT="left"
TEXT_ALIGN_RIGHT="right"
MAX_WIDTH=50

def chat_format_message(text: str, align: str = TEXT_ALIGN_LEFT, padding: int = 1) -> str:
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 > MAX_WIDTH:
            lines.append(current_line)
            current_line = word
        else:
            if current_line:
                current_line += " "
            current_line += word
    lines.append(current_line)

    max_line_width = max(len(line) for line in lines)
    frame_width = max_line_width + 2 * (padding + 1)

    top_bottom_frame = '+' + '-' * (frame_width - 2) + '+'
    horizontal_padding = '|' + ' ' * (frame_width - 2) + '|'

    formatted_lines = ['| ' + line.ljust(max_line_width) + ' |' for line in lines]

    frame = [top_bottom_frame] + [horizontal_padding] * padding + \
            formatted_lines + [horizontal_padding] * padding + \
            [top_bottom_frame]

    if align.lower() == TEXT_ALIGN_RIGHT:
        frame = [line.rjust(frame_width + len(lines[0])) for line in frame]

    return '\n'.join(frame)

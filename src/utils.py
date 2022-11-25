anki_newline_separator = r"<br>"

def slpit_lines_using_anki_separator(content: str):
    return content.split(anki_newline_separator)
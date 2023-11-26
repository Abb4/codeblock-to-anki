from pathlib import Path
import re
from parsed_callout import ParsedCallout
from utils import anki_newline_separator

from typing import List

class CalloutParser:
    def parse_text(self, text: str, path: Path) -> List:
        parsed_callouts = []
        current_callout: ParsedCallout = None

        lines = text.splitlines()

        for (line_number, line) in enumerate(lines):
            if not line.startswith(r">"):
                if current_callout is not None and current_callout.completed is False:
                    content = lines[current_callout.start_pos:line_number]

                    for (i, _) in enumerate(content):
                        content[i] = content[i][2:]

                    content = anki_newline_separator.join(content)

                    current_callout.complete(
                        content=content,
                        end_pos=line_number)

                    parsed_callouts.append(current_callout)
                    current_callout = None
                else:
                    continue

            if has_callout_header(line):
                (type, attributes) = parse_callout_header(line)

                current_callout = ParsedCallout()

                first_line_number = line_number + 1
                current_callout.begin(first_line_number, path, type, attributes)

        # FIXME ugly duplicate code
        if current_callout is not None and current_callout.completed is False:

            last_line = len(lines)

            content = lines[current_callout.start_pos:last_line]

            for (i, _) in enumerate(content):
                content[i] = content[i][2:]

            content = anki_newline_separator.join(content)

            current_callout.complete(
                content=content,
                end_pos=last_line)

            parsed_callouts.append(current_callout)
            current_callout = None

        return parsed_callouts

callout_header_template = re.compile(r"> \[!(\w*)\].? (.*)")

def has_callout_header(line: str):
    return callout_header_template.match(line) is not None

def parse_callout_header(line: str):
    matches = callout_header_template.findall(line)

    type = matches[0][0]

    attributes = []
    if len(matches[0]) > 1:
        attributes = matches[0][1].split(" ")

    return (type, attributes)
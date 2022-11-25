from pathlib import Path
import re
from parsed_callout import ParsedCallout
from parsed_codeblock import ParsedCodeBlock

class CalloutParser:
    def parse_text(self, text: str, path: Path) -> list:
        parsed_callouts = []
        current_callout: ParsedCallout = None
        
        for (line_number, line_raw) in enumerate(text.splitlines()):
            line = line_raw
            
            if not line.startswith(r">"):
                if current_callout is not None and current_callout.completed is False:
                    content = text.splitlines()[current_callout.start_pos:line_number]
                    
                    for (i, _) in enumerate(content):
                        content[i] = content[i][2:]
                    
                    content = "\n".join(content)
                    
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
            
            # if self.has_codeblock_separator(line):
            #     if current_codeblock == None or current_codeblock.is_completed():
            #         current_codeblock = ParsedCodeBlock()
                    
            #         type = self.parse_codeblock_type(line)
            #         headers = self.parse_codeblock_headers(line)
                    
            #         current_codeblock.begin(line_number + 1, path, type, headers)
            #     else:
            #         content = text.splitlines()[current_codeblock.start_pos:line_number]
            #         content = "\n".join(content)
                    
            #         current_codeblock.complete(
            #             content=content,
            #             end_pos=line_number)
                    
            #         parsed_codeblocks.append(current_codeblock)
            #         current_codeblock = None
           
        return parsed_callouts
       
    def has_codeblock_separator(self, line: str):
        return line.lstrip().startswith('```')
    
    def parse_codeblock_type(self, header_line: str):
        tail = header_line.lstrip()[3:]
        if len(tail) > 0:
            return tail.split(' ')[0].rstrip()
        
        return None

    def parse_codeblock_headers(self, header_line: str) -> list[str]:
        tail = header_line.lstrip()[3:]
        if len(tail) > 0:
            headers = tail.split(' ')
            
            for header in headers:
                header = header.strip()
            
            return headers[1:]
        
        return []

callout_header_template = re.compile(r"> \[!(\w*)\].? (.*)")

def has_callout_header(line: str):
    return callout_header_template.match(line) is not None

def parse_callout_header(line: str):
    matches = callout_header_template.findall(line)
    
    type = matches[0][0]
    
    attributes = []
    if len(matches) > 1:
        attributes = matches[0][1].split(" ")
    
    return (type, attributes)
from pathlib import Path
from parsed_codeblock import ParsedCodeBlock

from utils import anki_newline_separator

class CodeblockParser:
    def parse_text(self, text: str, path: Path) -> list:
        parsed_codeblocks = []
        current_codeblock: ParsedCodeBlock = None
        
        for (line_number, line_raw) in enumerate(text.splitlines()):
            line = line_raw
            
            if self.has_codeblock_separator(line):
                if current_codeblock == None or current_codeblock.is_completed():
                    current_codeblock = ParsedCodeBlock()
                    
                    type = self.parse_codeblock_type(line)
                    headers = self.parse_codeblock_headers(line)
                    
                    current_codeblock.begin(line_number + 1, path, type, headers)
                else:
                    content = text.splitlines()[current_codeblock.start_pos:line_number]
                    content = anki_newline_separator.join(content)
                    
                    current_codeblock.complete(
                        content=content,
                        end_pos=line_number)
                    
                    parsed_codeblocks.append(current_codeblock)
                    current_codeblock = None
           
        return parsed_codeblocks
       
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
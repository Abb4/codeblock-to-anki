import hashlib
from pathlib import Path
import genanki
from parsed_codeblock import ParsedCodeBlock

class DeckAssembler:
    def __init__(self):
        pass
    
    def assemble_deck_from_codeblocks(self, codeblocks: list[ParsedCodeBlock], output_path: Path):
        
        decks = {}
        
        for codeblock in codeblocks:
            note_name = self.get_attribute_from_codeblock_headers(codeblock.headers, "name")
        
            note_deck_name = self.get_attribute_from_codeblock_headers(codeblock.headers, "deck")
            
            assert note_name is not None
            assert note_deck_name is not None
            
            # TODO document on github how note ids are generated from names
            note = genanki.Note(
                guid=quick_hash(note_name + "_" + note_deck_name),
                model=genanki.CLOZE_MODEL,
                fields=[codeblock.content, '']
            )
           
            if note_deck_name in decks:
                decks[note_deck_name].add_note(note)
            else:
                # TODO document on github how deck ids are generated from deck name
                deck = genanki.Deck(
                    deck_id=quick_hash(note_deck_name),
                    name=note_deck_name
                )

                deck.add_note(note)
                
                print(f"Added {note_name} to deck {note_deck_name}")
                
                decks[note_deck_name] = deck
        
        package_name = "deck_package.apkg" 
        
        package_path = output_path / package_name 
         
        genanki.Package(decks.values()).write_to_file(package_path.absolute())
        
        print(f"Created {package_path.absolute()}")
   
    def get_attribute_from_codeblock_headers(self, headers: list[str], header_name: str):
        for header in headers:
            parts = header.split(":")
            key = parts[0]
            
            if key == header_name:
                if len(parts) > 1:
                    value = parts[1]
                    return value
                else:
                    return None
        
        return None

def quick_hash(str: str) -> int:
    # https://stackoverflow.com/questions/16008670/how-to-hash-a-string-into-8-digits
    return int(hashlib.sha1(str.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
import hashlib
from pathlib import Path
import genanki
from parsed_callout import ParsedCallout
from parsed_codeblock import ParsedCodeBlock

class DeckAssembler:
    def __init__(self):
        pass
    
    def add_notes_from_codeblocks(self, codeblocks: list[ParsedCodeBlock], decks: dict):
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
                
                print(f"Added {note_name} from codeblock to deck {note_deck_name}")
                
                decks[note_deck_name] = deck 
        

    def add_notes_from_callouts(self, callouts: list[ParsedCallout], decks: dict):
        for callout in callouts:
            note_name = self.get_attribute_value_by_name(callout.attributes, "name")
            
            note_deck_name = self.get_attribute_value_by_name(callout.attributes, "deck")
            
            if note_name == None or note_deck_name == None:
                continue
           
            # TODO document on github how note ids are generated from names
            note = genanki.Note(
                guid=quick_hash(note_name + "_" + note_deck_name),
                model=genanki.CLOZE_MODEL,
                fields=[callout.content, '']
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
                
                print(f"Added {note_name} from callout to deck {note_deck_name}")
                
                decks[note_deck_name] = deck 

    def get_attribute_value_by_name(self, attributes: list[str], attribute_name: str):
        for attribute in attributes:
            parts = attribute.split(":")
            key = parts[0]
            
            if key == attribute_name:
                if len(parts) > 1:
                    value = parts[1]
                    return value
                else:
                    return None
        
        return None
   
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
import genanki
from callout_parser import CalloutParser
from deck_assembler import DeckAssembler, quick_hash
from codeblock_parser import CodeblockParser
from utils import slpit_lines_using_anki_separator

def test_deck_creation():
    assembler = DeckAssembler()
    
    parser = CodeblockParser()
   
    content = '''```anki name:note1 deck:deck1
Contents Contents
Contents
```
some irrelevant text
> some irrelevant quote
```cpp
some irrelevant code
```

```anki name:note2 deck:deck1
    Contents2 Contents2
    Contents2
    Contents2 Contents2 Contents2
```

some irrelevant text
> some irrelevant quote
some irrelevant text

```cpp
some irrelevant code
```

```anki name:note3 deck:deck2
Contents3 Contents3
Contents3 Contents3 Contents3
```
'''
    
    codeblocks = parser.parse_text(content, None)

    decks: dict[str, genanki.Deck] = {}    
    
    assembler.add_notes_from_codeblocks(codeblocks, decks)
    
    assert len(decks.keys()) == 2
    
    deck1 = decks["deck1"]
    deck2 = decks["deck2"]
    
    assert deck1 is not None
    assert deck2 is not None
    
    assert len(deck1.notes) == 2
    assert len(deck2.notes) == 1
   
    note1: genanki.Note = deck1.notes[0] 
    note2: genanki.Note = deck1.notes[1] 
    note3: genanki.Note = deck2.notes[0] 
    
    note1_content = slpit_lines_using_anki_separator(note1.fields[0])
    note2_content = slpit_lines_using_anki_separator(note2.fields[0])
    note3_content = slpit_lines_using_anki_separator(note3.fields[0])

    assert len(note1_content) == 2
    assert len(note2_content) == 3
    assert len(note3_content) == 2
    
    assert note1_content[0].strip() == "Contents Contents"
    assert note1_content[1].strip() == "Contents"
    
    assert note2_content[0].strip() == "Contents2 Contents2"
    assert note2_content[1].strip() == "Contents2"
    assert note2_content[2].strip() == "Contents2 Contents2 Contents2"

    assert note3_content[0].strip() == "Contents3 Contents3"
    assert note3_content[1].strip() == "Contents3 Contents3 Contents3"

def test_deck_creation_from_callouts_by_deck_name():
    assembler = DeckAssembler()
    
    parser = CalloutParser()
   
    content = '''
> [!summary]+ name:note1 deck:deck1
> Contents Contents
> Contents
some irrelevant text
> some irrelevant quote
some irrelevant text

> [!summary]+ name:note2 deck:deck1
> Contents2 Contents2
> Contents2
> Contents2 Contents2 Contents2

some irrelevant text
> some irrelevant quote
some irrelevant text

> [!summary]+ name:note3 deck:deck2
> Contents3 Contents3
> Contents3 Contents3 Contents3
'''
    
    callouts = parser.parse_text(content, None)

    decks: dict[str, genanki.Deck] = {}    
    
    assembler.add_notes_from_callouts(callouts, decks)
    
    assert len(decks.keys()) == 2
    
    deck1 = decks["deck1"]
    deck2 = decks["deck2"]
    
    assert deck1 is not None
    assert deck2 is not None
    
    assert len(deck1.notes) == 2
    assert len(deck2.notes) == 1
   
    note1: genanki.Note = deck1.notes[0] 
    note2: genanki.Note = deck1.notes[1] 
    note3: genanki.Note = deck2.notes[0] 
    
    note1_content = slpit_lines_using_anki_separator(note1.fields[0])
    note2_content = slpit_lines_using_anki_separator(note2.fields[0])
    note3_content = slpit_lines_using_anki_separator(note3.fields[0])

    assert len(note1_content) == 2
    assert len(note2_content) == 3
    assert len(note3_content) == 2
    
    assert note1_content[0].strip() == "Contents Contents"
    assert note1_content[1].strip() == "Contents"
    
    assert note2_content[0].strip() == "Contents2 Contents2"
    assert note2_content[1].strip() == "Contents2"
    assert note2_content[2].strip() == "Contents2 Contents2 Contents2"

    assert note3_content[0].strip() == "Contents3 Contents3"
    assert note3_content[1].strip() == "Contents3 Contents3 Contents3"


def test_quick_hash():
    note1_name = "My Note"
    note2_name = "My Note" # test that hashes correctly use values for equality
    note3_name = "My other Note"
    
    assert quick_hash(note1_name) == quick_hash(note2_name)
    assert quick_hash(note1_name) != quick_hash(note3_name)
    
def test_getting_attributes_from_headers():
    assembler = DeckAssembler()
    
    attributes = ["attribute1:value1", "attribute2:value2", "attribute3"]
    
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute1") == "value1"
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute2") == "value2"
    assert assembler.get_attribute_from_codeblock_headers(attributes, "attribute3") == None
    assert assembler.get_attribute_from_codeblock_headers(attributes, "unknown") == None

def test_getting_attribute_values():
    assembler = DeckAssembler()
    
    attributes = ["attribute1:value1", "attribute2:value2", "attribute3"]
    
    assert assembler.get_attribute_value_by_name(attributes, "attribute1") == "value1"
    assert assembler.get_attribute_value_by_name(attributes, "attribute2") == "value2"
    assert assembler.get_attribute_value_by_name(attributes, "attribute3") == None
    assert assembler.get_attribute_value_by_name(attributes, "unknown") == None
    
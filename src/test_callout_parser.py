from callout_parser import CalloutParser
from parsed_callout import ParsedCallout

from utils import split_lines_using_anki_separator

def test_parsing_of_one_callout():
    parser = CalloutParser()

    content = '''
some irrelevant text
> some irrelevant quote

> [!NOTE] Title attribute1:value1 attribute2:value2 attribute3
> Contents Contents
> Contents2
some irrelevant text
> some irrelevant quote
some irrelevant text
    '''
    
    callouts = parser.parse_text(content, path=None)
    
    assert len(callouts) == 1
    
    callout1: ParsedCallout = callouts[0]
   
    assert callout1.type == "NOTE"
     
    callout1_content = split_lines_using_anki_separator(callout1.content)
    
    assert len(callout1_content) == 2
    
    assert callout1_content[0].strip() == "Contents Contents"
    assert callout1_content[1].strip() == "Contents2"
    
    callout1_attributes = callout1.attributes
    
    assert len(callout1_attributes) == 4
    
    assert callout1_attributes[0] == "Title"
    assert callout1_attributes[1] == "attribute1:value1"
    assert callout1_attributes[2] == "attribute2:value2"
    assert callout1_attributes[3] == "attribute3"


def test_parsing_of_multiple_callouts():
    parser = CalloutParser()

    content = '''
some irrelevant text
> some irrelevant quote

> [!NOTE] Title attribute1:value1 attribute2:value2 attribute3
> Contents Contents
> Contents
some irrelevant text
> some irrelevant quote
some irrelevant text

> [!WARNING] Title2 attribute22:value22
> Contents2 Contents2
> Contents2
> Contents2 Contents2 Contents2
    '''
    
    callouts = parser.parse_text(content, path=None)
    
    assert len(callouts) == 2
    
    callout1 = callouts[0]
    callout2 = callouts[1]
    
    assert callout1.type == "NOTE"
    assert callout2.type == "WARNING"
    
    callout1_content = split_lines_using_anki_separator(callout1.content)
    callout2_content = split_lines_using_anki_separator(callout2.content)
    
    assert len(callout1_content) == 2
    
    assert callout1_content[0].strip() == "Contents Contents"
    assert callout1_content[1].strip() == "Contents"
    
    assert len(callout2_content) == 3
    
    assert callout2_content[0].strip() == "Contents2 Contents2"
    assert callout2_content[1].strip() == "Contents2"
    assert callout2_content[2].strip() == "Contents2 Contents2 Contents2"

    callout1_attributes = callout1.attributes
    callout2_attributes = callout2.attributes

    assert len(callout1_attributes) == 4
    
    assert callout1_attributes[0] == "Title"
    assert callout1_attributes[1] == "attribute1:value1"
    assert callout1_attributes[2] == "attribute2:value2"
    assert callout1_attributes[3] == "attribute3"

    
    assert len(callout2_attributes) == 2
    
    assert callout2_attributes[0] == "Title2"
    assert callout2_attributes[1] == "attribute22:value22"
    
    

def test_parsing_of_one_callout2():
    parser = CalloutParser()

    content = '''
> [!summary]+ name:test_note deck:test_deck
> {{c1: Strings}} are {{c2: Nice}}
> Some More Content'''
    
    callouts = parser.parse_text(content, path=None)
    
    assert len(callouts) == 1
    
    callout1: ParsedCallout = callouts[0]
   
    assert callout1.type == "summary"
     
    callout1_content = split_lines_using_anki_separator(callout1.content)
    
    assert len(callout1_content) == 2
    
    assert callout1_content[0].strip() == "{{c1: Strings}} are {{c2: Nice}}"
    assert callout1_content[1].strip() == "Some More Content"
    
    callout1_attributes = callout1.attributes
    
    assert len(callout1_attributes) == 2
    
    assert callout1_attributes[0] == "name:test_note"
    assert callout1_attributes[1] == "deck:test_deck"
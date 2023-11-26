import argparse
from pathlib import Path

import genanki
from callout_parser import CalloutParser

from deck_assembler import DeckAssembler
from parsed_callout import ParsedCallout
from parsed_codeblock import ParsedCodeBlock
from codeblock_parser import CodeblockParser

DEFAULT_PACKAGE_NAME = "deck_package.apkg"

def main():
    parser = argparse.ArgumentParser(description='Parses markdown elements into cloze anki notes and assembles them into an anki package.')
    parser.add_argument('--input_dir', type=str, help='Input directory of the markdown files to parse. If none provided, defaults to current directory.')
    parser.add_argument('--output_dir', type=str, help='Output directory of the resulting anki package. If none provided, defaults to input_dir.')
    parser.add_argument('--package_name', type=str, default=DEFAULT_PACKAGE_NAME, help=f'The name of the resulting package (default: {DEFAULT_PACKAGE_NAME})')

    args = parser.parse_args()

    input_dir = Path(args.input_dir) if args.input_dir else Path(".")
    output_dir = Path(args.output_dir) if args.output_dir else Path(input_dir)
    package_name = args.package_name

    package_path = output_dir / package_name

    assert input_dir.exists(), f'given input_dir {input_dir} does not exist'
    assert input_dir.is_dir(), f'given input_dir {input_dir} is not a valid directory'

    assert output_dir.exists(), f'given output_dir {output_dir} does not exist'
    assert output_dir.is_dir(), f'given output_dir {output_dir} is not a valid directory'

    assembler = DeckAssembler()
    codeblock_parser = CodeblockParser()
    callout_parser = CalloutParser()

    codeblocks: list[ParsedCodeBlock] = []
    callouts: list[ParsedCallout] = []

    files = list(input_dir.glob("./**/*.md"))

    print(f"Checking {len(files)} files...")

    for file in files:
        with file.open("r") as f:

            contents = f.read()

            codeblocks.extend(
                codeblock_parser.parse_text(contents, path=file)
            )

            callouts.extend(
                callout_parser.parse_text(contents, path=file)
            )

    print(f"Found 'anki' {len(codeblocks)} codeblocks")

    print(f"Found {len(callouts)} callouts")

    decks = {}

    assembler.add_notes_from_codeblocks(codeblocks, decks)
    assembler.add_notes_from_callouts(callouts, decks)

    genanki.Package(decks.values()).write_to_file(package_path.absolute())

    print(f"Created {package_path.absolute()}")

if __name__=="__main__":
    main()
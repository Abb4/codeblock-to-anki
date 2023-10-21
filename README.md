# markdown-to-anki
Parses markdown elements into cloze anki notes and assembles them into an anki package using [genanki](https://github.com/kerrickstaley/genanki).

## Usage
This script can handle codeblocks or [obsidian callouts](https://help.obsidian.md/How+to/Use+callouts).

Create some anki code blocks or callouts in your markdown files with unique `name` and `deck` (note the `anki` attribute in codeblock):

~~~markdown
```anki name:strings deck:programming_fundamentals
	{{c1::Strings}} are sequences of {{c2::characters}}.
```

or using markdown codeblock:

```markdown anki name:strings deck:programming_fundamentals
	{{c1::Strings}} are sequences of {{c2::characters}}.
```

Note the `anki` attribute in the header of the codeblock. It is required.

Some text..

> [!summary]+ name:obsidian deck:general
> Use {{c1:obsidian}} to record notes
>
> Because its convenient.
~~~

Run `python path/to/src/markdown_to_anki.py` in the directory where you notes lie. All notes in the directory and child directories will be assembled into anki cloze notes and written into a package.

Import the package into anki.

If you want other markdown elements to be handled, feel free to submit an issue.

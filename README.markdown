yml2tex
=======

yml2tex is a simple python script which generates LaTeX Beamer code 
out of YAML files.

Requirements
------------

- [PyYAML][pyyaml] 3.07
- [Pygments][pygments] 1.0 (Optional, used for syntax highlighting)

Usage
-----

Pass yml2tex a YAML file as the first argument. The output will
be printed to stdout.

    yml2tex foobar.yml > foobar.tex
    
The document can then be compiled:

    pdflatex foobar.tex

Structure
---------

Since LaTeX Beamer presentations are structured in sections, subsections 
and frames, the YAML file must have the following structure:

    Introduction:
        About this presentation:
            Author:
                - Name
                - Age
                - Occupation
                
*"Introduction"* would be the title of the section, *"About this presentation"* 
the title of the subsection and *"Author"* the frame title. 
*"Name"*, *"Age"* and *"Occupation"* would be items in a list.

Nested Items
------------

Each item can have other items associated.

    Introduction:
        About this presentation:
            Author:
                - Name
                - Age
                - Occupation:
                    - 2001 to 2009 Company A
                    - 2009 Company Z

The script doesn't limit the depth of nested items, however LaTeX Beamer 
does limit it up to three items.

Note: The items that start with *+* sign will be displayed together with the
frame title. All others will be displayed after a pause.

Images
------

It's possible to create a frame with an image in it by using the 
"image" keyword followed by the image path as a frame title.

    Features:
      Images:
        image bar:
        image foo:
            width: 10cm
            height: 30cm

In the above example, two frames would be created that include 
the *"bar"* and *"foo"* image.

Please note to not specify the file extension. The *"\pgfimage"* extension
in LaTeX automatically searches for JPG and PNG files.

Options will be passed directly to the \pgfimage command, the supported
options as of writing this are:

* width
* height
* page
* interpolate
* mask

If no options are specified, the image will be the same size as the frame.

Metadata
--------

It's possible to specify metadata for the document in the YAML file itself.

To do this, create a "metas" key at the top of the YAML file. The supported
options are:

* **title** *(string)* If not specified, 'Example Presentation' is used.
* **short_title** *(string)* Short title to appear on top. If not specified, the contents of **title** is used.
* **author** *(string)* If not specified, 'Arthur Koziel' is used.
* **institute** *(string)* If not specified, nothing is used.
* **date** *(string)* If not specified, current date is used.
* **outline** *(boolean)* If an Outline/Table of contents should be generated. True if not specified.
* **highlight\_style** *(string)* Pygments style for code highlighting. If not specified 'default' is used.
* **outline_name** *(string)* Custom outline text. If not specified, 'Outline' is used.
* **theme** *(string)* Theme to use. If not specified, 'Antibes' is used.

Example:

    metas:
        title: My First Presentation
        short_title: Presentation
        author: Arthur Koziel
        institute: FH-Dortmund
        date: 14.11.2008
        outline: False
        highlight_style: colorful
        outline_name: Contents

Code Highlighting
-----------------

It is possible to include source code in a frame and highlight it (if Pygments
is available). If Pygments is not available the source code will still be
included but not highlighted.

Per default Pygments *"default"* style is used. You can change it by
specifying a *"highlight\_style"* in the Metadata. The Pygments Lexer is guessed 
by the filename.

To include the source code of a file, use the *"include"* keyword followed by 
the filepath as a frame title. The path of the file must be relative to the
YAML file's path.

This example below would include and highlight the contents of *"foobar.py"*.

    Features:
        Code Highlighting:
            include foobar.py:

[pyyaml]: http://pyyaml.org/
[pygments]: http://pygments.org/

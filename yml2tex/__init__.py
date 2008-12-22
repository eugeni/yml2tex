#!/usr/bin/env python
# encoding: utf-8
"""Transform a YAML file into a LaTeX Beamer presentation.

Usage: bin/yml2tex input.yml > output.tex
"""

__version__ = '1.2'
__author__ = 'Arthur Koziel <arthur@arthurkoziel.com>'
__url__ = 'http://code.google.com/p/yml2tex/'

from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import LatexFormatter

import yaml

from loader import PairLoader

def section(title):
    """
    Given the section title, return its corresponding LaTeX command.
    """
    return '\n\n\section{%s}' % _escape_output(title)

def subsection(title):
    """
    Given the subsection title, return its corresponding LaTeX command.
    """
    return '\n\subsection{%s}' % _escape_output(title)

def frame(title, items):
    """
    Given the frame title and corresponding items, delegate to the appropriate 
    function and returns its LaTeX commands.
    """
    if title.startswith('include'):
        out = code(title)
    elif title.startswith('image'):
        out = image(title, items)
    else:
        out = "\n\\frame {"
        out += "\n\t\\frametitle{%s}" % _escape_output(title)
        out += itemize(items)
        out += "\n}"
    return out

def _escape_output(text):
    """Escape special characters in Latex"""
    dic = {'&': '\&', 
           '$': '\$', 
           '%': '\%', 
           '#': '\#', 
           '_': '\_', 
           '{': '\{', 
           '}': '\}'}
    
    for i, j in dic.iteritems():  
        text = text.replace(i, j)
    return text

def itemize(items):
    """
    Given the items for a frame, returns the LaTeX syntax for an itemized list.
    If an item itself is a list, a nested itemized list will be created.
    
    The script itself doesn't limit the depth of nested lists. LaTeX Beamer 
    limits lists to be nested up to a depth of 3.
    """
    out = "\n\t\\begin{itemize}[<+-| alert@+>]"
    for item in items:
        if isinstance(item, list):
            for i in item:
                out += "\n\t\\item %s" % _escape_output(item[0][0])
                out += itemize(item[0][1])
        else:
            out += "\n\t\\item %s" % _escape_output(item)
    out += "\n\t\end{itemize}"
    return out

def code(title):
    """
    Return syntax highlighted LaTeX.
    """
    filename = title.split(' ')[1]
    
    try:
        lexer = get_lexer_for_filename(filename)
    except:
        lexer = get_lexer_by_name('text')
    
    f = open(filename, 'r')
    code = highlight(f.read(), lexer, LatexFormatter())
    f.close()
    
    out = "\n\\begin{frame}[fragile,t]"
    out += "\n\t\\frametitle{Code: \"%s\"}" % filename
    out += code
    out += "\n\end{frame}"
    return out

def image(title, options):
    """
    Given a frame title, which starts with "image" and is followed by the image 
    path, return the LaTeX command to include the image.
    """
    if not options:
        options = ""
    options = ",".join(["%s=%s" % (k, v) for k, v in dict(options).items()])
    
    out = "\n\\frame[shrink] {"
    out += "\n\t\\pgfimage[%s]{%s}" % (options, title.split(' ')[1])
    out += "\n}"
    return out

def header(metas):
    """
    Return the LaTeX Beamer document header declarations.
    """

    out = "\documentclass[slidestop,red]{beamer}"
    out += "\n\usepackage[utf8]{inputenc}"
    out += "\n\usepackage{fancyvrb,color}\n\n"
    
    # generate style definitions for pygments syntax highlighting
    out += LatexFormatter(style=metas.get('highlight_style', 'default')).get_style_defs()

    out += "\n\n\usetheme{Antibes}"
    out += "\n\setbeamertemplate{footline}[frame number]"
    out += "\n\usecolortheme{lily}"
    out += "\n\\beamertemplateshadingbackground{blue!5}{yellow!10}"
    
    out += "\n\n\\title{%s}" % metas.get('title', 'Example Presentation')
    out += "\n\\author{%s}" % metas.get('author', 'Arthur Koziel')
    out += "\n\\institute{%s}" % metas.get('institute', '')
    out += "\n\date{%s}" % metas.get('date', '\\today')
    out += "\n\n\\begin{document}"
    out += "\n\n\\frame{\\titlepage}"
    
    if metas.get('outline', True):
        out += "\n\n\section*{Outline}"
        out += "\n\\frame {"
        out += "\n\t\\frametitle{Outline}"
        out += "\n\t\\tableofcontents"
        out += "\n}"

        out += "\n\n\AtBeginSection[] {"
        out += "\n\t\\frame{"
        out += "\n\t\t\\frametitle{Outline}"
        out += "\n\t\t\\tableofcontents[currentsection]"
        out += "\n\t}"
        out += "\n}"
    return out

def footer():
    """
    Return the LaTeX Beamer document footer.
    """
    out = "\n\end{document}"
    return out
    
def main(file):
    """
    Return the final LaTeX presentation after invoking all necessary functions.
    """
    doc = yaml.load(file, Loader=PairLoader)
    
    metas = {}
    if doc[0][0] == 'metas':
        metas = dict(doc[0][1])
        del doc[0]
    
    out = header(metas)
    for sections, doc in doc:
        out += section(sections)
        for subsections, doc in doc:
            out += subsection(subsections)
            for frames, items in doc:
                out += frame(frames, items)
    out += footer()
    return out.encode('utf-8')
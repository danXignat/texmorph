from enum import IntEnum, StrEnum, Enum

class SectionLevelType(IntEnum):
    """Section levels in LaTeX documents"""
    SECTION      : int = 1
    SUBSECTION   : int = 2
    SUBSUBSECTION: int = 3
    PARAGRAPH    : int = 4

class DocumentClassType(StrEnum):
    """Supported LaTeX document classes"""
    ARTICLE     : str = "article"
    IEEE        : str = "IEEEtran"
    SPRINGER    : str = "sn-jn"
    # ACM: str = "acmart"
    # ELSEVIER: str = "elsarticle"

class FormatType(Enum):
    """"""
    ARTICLE: str = "article"
    IEEE: str = "IEEE"
    SPRINGER: str = "Springer Nature"

class ElementType(StrEnum):
    """Types of elements in LaTeX documents"""
    PACKAGE         : str = "package"
    DOCUMENT_CLASS  : str = "document_class"
    AUTHOR          : str = "author"
    SECTION         : str = "section"
    FIGURE          : str = "figure"
    TABLE           : str = "table"
    REFERENCE       : str = "reference"
    TITLE           : str = "title"
    ABSTRACT        : str = "abstract"
    SUBSECTION      : str = "subsection"
    SUBSUBSECTION   : str = "subsubsection"
    PARAGRAPH       : str = "paragraph"
    EQUATION        : str = "equation"
    MATH            : str = "math"
    ITEMIZE         : str = "itemize"
    ENUMERATE       : str = "enumerate"
    DEFINITION      : str = "definition"
    THEOREM         : str = "theorem"
    PROOF           : str = "proof"
    ALGORITHM       : str = "algorithm"
    FOOTNOTE        : str = "footnote"
    CITATION        : str = "citation"
    HYPERLINK       : str = "hyperlink"
    BIBLIOGRAPHY    : str = "bibliography"
    APPENDIX        : str = "appendix"
    DATE            : str = "date"
    COMMAND         : str = "command"
    ENVIRONMENT     : str = "environment"
    CODE_BLOCK      : str = "code_block"
    INCLUDE         : str = "include"
    GLOSSARY        : str = "glossary"
    INDEX           : str = "index"
    HEADER          : str = "header"
    FOOTER          : str = "footer"
    PAGE_NUMBER     : str = "page_number"
    MARGIN_NOTE     : str = "margin_note"
    TOC             : str = "table_of_contents"
    LIST_OF_FIGURES : str = "list_of_figures"
    LIST_OF_TABLES  : str = "list_of_tables"
    NEWPAGE         : str = "newpage"
    COLOR           : str = "color"
    BOX             : str = "box"
    COLUMN          : str = "column"
    TEXT            : str = "text"

    OTHER           : str = "other"

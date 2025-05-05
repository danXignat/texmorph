from typing import Optional, Any

import datetime as dt
from pydantic import BaseModel, Field

from models.types import DocumentClassType, FormatType

class NormalisedNode(BaseModel):
    """Base class for normalized elements"""
    original_content: str

    children: list['NormalisedNode'] = Field(default_factory=list)
    parent: Optional['NormalisedNode'] = None


    def __str__(self):
        cls_name = self.__class__.__name__

        return f"{cls_name}({self.children})"

    def __repr__(self):
        return str(self)

class Text(NormalisedNode):
    """Text in normalized format"""
    text: str

class Package(NormalisedNode):
    """Package in normalized format"""
    names   : list[str]
    options : list[str] = Field(default_factory=list)

class DocumentClass(NormalisedNode):
    type    : DocumentClassType
    options : list[str] = Field(default_factory=list)

class Author(NormalisedNode):
    """Author information in normalized format"""
    name        : str
    affiliation : str | None = None
    email       : str | None = None
    orcid       : str | None = None

class Title(NormalisedNode):
    """Document title in normalized format"""
    title   : str
    subtitle: str | None = None

class Section(NormalisedNode):
    """Document section in normalized format"""
    title       : str
    content     : str
    level       : int = 1
    subsections : list['Section'] = Field(default_factory=list)

class Figure(NormalisedNode):
    """Figure in normalized format"""
    filename: str
    caption : str | None = None
    label   : str | None = None
    width   : str | None = None
    height  : str | None = None

class MathFormula(NormalisedNode):
    """Math formula in normalized format"""
    formula: str
    label  : str

#--------table-------
class TableCell(BaseModel):
    content: Any
    rowspan: int = 1
    colspan: int = 1

class Table(NormalisedNode):
    """
    Represents a table in a normalized format.

    Attributes:
        cells (list[list[TableCell]]): A 2D list of TableCell objects, representing the structure of the table's rows and columns.
        caption (str | None): An optional caption for the table.
        content (str | None): Optional content or description of the table.
        label (str | None): An optional label for referencing the table.
    """
    cells: list[list[TableCell]]

    caption: str | None = None
    content: str | None = None
    label: str | None = None
#------------------------------

class Abstract(NormalisedNode):
    """Document abstract in normalized format"""
    content: str

class Date(NormalisedNode):
    """Date information in normalized format"""
    date: dt.date

class Keywords(NormalisedNode):
    """Keywords in normalized format"""
    words: list[str] = Field(default_factory=list)

class Reference(NormalisedNode):
    """Reference in normalized format"""
    ENTRYTYPE: FormatType
    # citation_key: str = Field(..., description="Unique identifier for the reference")

    ID           : str | None = None
    title        : str | None = None
    author       : str | None = None
    editor       : str | None = None
    journal      : str | None = None
    publisher    : str | None = None
    year         : str | None = None
    volume       : str | None = None
    number       : str | None = None
    pages        : str | None = None
    month        : str | None = None
    note         : str | None = None

    # Additional fields
    address      : str | None = None
    booktitle    : str | None = None
    chapter      : str | None = None
    edition      : str | None = None
    howpublished : str | None = None
    institution  : str | None = None
    organization : str | None = None
    school       : str | None = None
    series       : str | None = None
    type         : str | None = None


    additional_fields: dict[str, str] = Field(default_factory=dict)

class Other(NormalisedNode):
    """Other information in normalized format"""
    name: str
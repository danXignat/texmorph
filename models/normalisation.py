from typing import Optional, Any, List

import datetime as dt
from pydantic import BaseModel, Field

from models.types import FormatType

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
    type    : FormatType
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
        rows (List[List[TableCell]]): List of Lists of TableCell objects representing the rows of the table.
        caption (Optional[str]): An optional caption for the table.
        content (Optional[str]): Optional content or description of the table.
        label (Optional[str]): An optional label for referencing the table.
    """
    rows    : List[List[TableCell]]

    caption : Optional[str] = None
    content : Optional[str] = None
    label   : Optional[str] = None
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
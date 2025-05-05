from pydantic import BaseModel, Field

from models.elements import Package, DocumentClass
from models.types import DocumentClassType

class FormatRule(BaseModel):
    """Base class for format rules"""
    description: str
    example: str

class SectionNumberRule(FormatRule):
    """Rule for section numbering"""
    numbering_scheme: str

class ReferenceFormatRule(FormatRule):
    """Rule for reference formatting"""
    style: str  # e.g., "numbered" or "author-year"
    bibtex_style: str  # e.g., "IEEEtran", "spmpsci"

class AuthorFormatRule(FormatRule):
    """Rule for author formatting"""
    format_command: str  # LaTeX command to format authors

class FormatRules(BaseModel):
    """Collection of format rules"""
    document_class: DocumentClass
    paper_size: str
    margins: str
    font: str
    section_numbering: SectionNumberRule
    reference_format: ReferenceFormatRule
    author_format: AuthorFormatRule
    required_packages: list[str] = Field(default_factory=list)
    additional_commands: list[str] = Field(default_factory=list)


IEEE_RULES = FormatRules(
    document_class=DocumentClass(type=DocumentClassType.IEEE, options=["conference"]),
    paper_size="US Letter (8.5 × 11 inches)",
    margins="1 inch all sides",
    font="Times New Roman, 10-point",
    section_numbering=SectionNumberRule(
        description="IEEE uses Roman numerals for main sections, letters for subsections",
        numbering_scheme="I, II, III for sections; A, B, C for subsections",
        example="I. Introduction → A. Background"
    ),
    reference_format=ReferenceFormatRule(
        description="IEEE uses numbered references in square brackets",
        style="numbered",
        bibtex_style="IEEEtran",
        example="[1] J. Smith, \"Paper Title,\" Journal Name, vol. 1, no. 1, pp. 1-10, 2023."
    ),
    author_format=AuthorFormatRule(
        description="IEEE uses IEEEauthorblockN and IEEEauthorblockA commands",
        format_command="\\author{\\IEEEauthorblockN{Name}\\IEEEauthorblockA{Affiliation\\\\Email}}",
        example="\\author{\\IEEEauthorblockN{John Smith}\\IEEEauthorblockA{University\\\\Email}}"
    ),
    required_packages=[
        Package("cite"),
        Package("amsmath,amssymb,amsfonts"),
        Package("algorithmic"),
        Package("graphicx"),
        Package("textcomp"),
        Package("xcolor")
    ],
    additional_commands=[
        "\\IEEEoverridecommandlockouts"
    ]
)

SPRINGER_RULES = FormatRules(
    document_class=DocumentClass(type=DocumentClassType.SPRINGER, options=["pdflatex", "sn-mathphys-num"]),
    paper_size="A4 (210 × 297 mm)",
    margins="2.5 cm all sides",
    font="Times New Roman, 10-12 point",
    section_numbering=SectionNumberRule(
        description="Springer uses decimal numbering for sections",
        numbering_scheme="1, 1.1, 1.1.1",
        example="1. Introduction → 1.1 Background"
    ),
    reference_format=ReferenceFormatRule(
        description="Springer typically uses author-year references",
        style="author-year",
        bibtex_style="spmpsci",
        example="Smith (2023) states that... OR The study (Smith, 2023) shows..."
    ),
    author_format=AuthorFormatRule(
        description="Springer uses separate author and institute commands",
        format_command="\\author{Name}\\institute{Affiliation}\\email{Email}",
        example="\\author{John Smith}\\institute{University}\\email{john@example.com}"
    ),
    required_packages=[
        Package("graphicx"),
        Package("multirow"),
        Package("amsmath,amssymb,amsfonts"),
        Package("amsthm"),
        Package("mathrsfs"),
        Package("appendix", options=["title"]),
        Package("xcolor"),
        Package("textcomp"),
        Package("manyfoot"),
        Package("booktabs"),
        Package("algorithm"),
        Package("algorithmicx"),
        Package("algpseudocode"),
        Package("listings")
    ]
)
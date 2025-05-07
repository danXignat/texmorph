from unittest import case

from TexSoup import TexNode

from models.types import FormatType
from models.normalisation import *

from core.mapping import *
import utils.extraction as extraction
from formats.IFormat import IEEEFormat, SNFormat, FORMATS, IFormat
from rag.extraction import RAGExtractor
from config.settings import Settings

class Normaliser:
    def __init__(self, format_type: FormatType):
        self._format_type = format_type

        match format_type:
            case FormatType.ARTICLE:
                pass

            case FormatType.IEEE:
                self._format = IEEEFormat()

            case FormatType.SPRINGER:
                self._format = SNFormat()

            case _:
                raise ValueError(f"Unsupported format type: {format_type}")

        self._normalise = {
            ElementType.PACKAGE: self._normalise_package,
            ElementType.DOCUMENT_CLASS: self._normalise_document_class,
            ElementType.AUTHOR: self._normalise_author,
            ElementType.SECTION: self._normalise_section,
            ElementType.FIGURE: self._normalise_figure,
            ElementType.TABLE: self._normalise_table,
            ElementType.REFERENCE: self._normalise_reference,
            ElementType.TITLE: self._normalise_title,
            ElementType.ABSTRACT: self._normalise_abstract,
            ElementType.SUBSECTION: self._normalise_subsection,
            ElementType.SUBSUBSECTION: self._normalise_subsubsection,
            ElementType.PARAGRAPH: self._normalise_paragraph,
            ElementType.EQUATION: self._normalise_equation,
            ElementType.MATH: self._normalise_math,
            ElementType.ITEMIZE: self._normalise_itemize,
            ElementType.ENUMERATE: self._normalise_enumerate,
            ElementType.DEFINITION: self._normalise_definition,
            ElementType.THEOREM: self._normalise_theorem,
            ElementType.PROOF: self._normalise_proof,
            ElementType.ALGORITHM: self._normalise_algorithm,
            ElementType.FOOTNOTE: self._normalise_footnote,
            ElementType.CITATION: self._normalise_citation,
            ElementType.HYPERLINK: self._normalise_hyperlink,
            ElementType.BIBLIOGRAPHY: self._normalise_bibliography,
            ElementType.APPENDIX: self._normalise_appendix,
            ElementType.DATE: self._normalise_date,
            ElementType.COMMAND: self._normalise_command,
            ElementType.ENVIRONMENT: self._normalise_environment,
            ElementType.CODE_BLOCK: self._normalise_code_block,
            ElementType.INCLUDE: self._normalise_include,
            ElementType.GLOSSARY: self._normalise_glossary,
            ElementType.INDEX: self._normalise_index,
            ElementType.HEADER: self._normalise_header,
            ElementType.FOOTER: self._normalise_footer,
            ElementType.PAGE_NUMBER: self._normalise_page_number,
            ElementType.MARGIN_NOTE: self._normalise_margin_note,
            ElementType.TOC: self._normalise_table_of_contents,
            ElementType.LIST_OF_FIGURES: self._normalise_list_of_figures,
            ElementType.LIST_OF_TABLES: self._normalise_list_of_tables,
            ElementType.NEWPAGE: self._normalise_newpage,
            ElementType.COLOR: self._normalise_color,
            ElementType.BOX: self._normalise_box,
            ElementType.COLUMN: self._normalise_column,
            ElementType.OTHER: self._normalise_other,
            ElementType.TEXT: self._normalise_text,
        }

    def normalise(self, node: TexNode | str) -> NormalisedNode:
        if isinstance(node, str):
            return self._normalise_text(node)

        type: ElementType = DEFAULT_DICT.get(node.name, None)

        if type is None:
            type = ElementType.OTHER

        return self._normalise[type](node)

    def _normalise_text(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX text node."""
        return Text(
            text=str(node),
            original_content=str(node),
        )

    def _normalise_package(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX package node."""
        return Package(
            names=extraction.get_required(node),
            options=extraction.get_optionals(node),
            original_content=str(node),
        )

    def _normalise_document_class(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX document class node."""
        return DocumentClass(
            type=FormatType(extraction.get_required(node)[0]),
            options=extraction.get_optionals(node),
            original_content=str(node),
        )

    def _normalise_author(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX author node."""
        return Author(
            name=extraction.get_required(node)[0],
            original_content=str(node),
        )


    def _normalise_section(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX section node."""
        return Section(
            title=extraction.get_required(node)[0],
            content="",
            level=1,
            original_content=str(node),
        )

    def _normalise_subsection(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX subsection node."""
        return Section(
            title=extraction.get_required(node)[0],
            content="",
            level=2,
            original_content=str(node),
        )

    def _normalise_subsubsection(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX subsubsection node."""
        return Section(
            title=extraction.get_required(node)[0],
            content="",
            level=3,
            original_content=str(node),
        )

    def _normalise_figure(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX figure node."""
        graphics: TexNode = node.includegraphics

        return Figure(
            filename= extraction.get_required(graphics)[0],
            original_content=str(node),
        )

    def _normalise_table(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX table node."""
        extractor = RAGExtractor()

        table: NormalisedNode = extractor.extract(ElementType.TABLE, str(node), Table)

        return table

    def _normalise_reference(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX reference node."""
        # Implementation here
        pass

    def _normalise_title(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX title node."""
        return Title(
            title=extraction.get_required(node)[0],
            original_content=str(node),
        )

    def _normalise_abstract(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX abstract node."""
        # Implementation here
        pass

    def _normalise_paragraph(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX paragraph node."""
        # Implementation here
        pass

    def _normalise_equation(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX equation node."""
        # Implementation here
        pass

    def _normalise_math(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX math node."""
        # Implementation here
        pass

    def _normalise_itemize(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX itemize node."""
        # Implementation here
        pass

    def _normalise_enumerate(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX enumerate node."""
        # Implementation here
        pass

    def _normalise_definition(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX definition node."""
        # Implementation here
        pass

    def _normalise_theorem(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX theorem node."""
        # Implementation here
        pass

    def _normalise_proof(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX proof node."""
        # Implementation here
        pass

    def _normalise_algorithm(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX algorithm node."""
        # Implementation here
        pass

    def _normalise_footnote(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX footnote node."""
        # Implementation here
        pass

    def _normalise_citation(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX citation node."""
        # Implementation here
        pass

    def _normalise_hyperlink(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX hyperlink node."""
        # Implementation here
        pass

    def _normalise_bibliography(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX bibliography node."""
        # Implementation here
        pass

    def _normalise_appendix(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX appendix node."""
        # Implementation here
        pass

    def _normalise_date(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX date node."""
        # Implementation here
        pass

    def _normalise_command(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX command node."""
        # Implementation here
        pass

    def _normalise_environment(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX environment node."""
        # Implementation here
        pass

    def _normalise_code_block(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX code block node."""
        # Implementation here
        pass

    def _normalise_include(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX include node."""
        # Implementation here
        pass

    def _normalise_glossary(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX glossary node."""
        # Implementation here
        pass

    def _normalise_index(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX index node."""
        # Implementation here
        pass

    def _normalise_header(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX header node."""
        # Implementation here
        pass

    def _normalise_footer(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX footer node."""
        # Implementation here
        pass

    def _normalise_page_number(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX page number node."""
        # Implementation here
        pass

    def _normalise_margin_note(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX margin note node."""
        # Implementation here
        pass

    def _normalise_table_of_contents(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX table of contents node."""
        # Implementation here
        pass

    def _normalise_list_of_figures(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX list of figures node."""
        # Implementation here
        pass

    def _normalise_list_of_tables(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX list of tables node."""
        # Implementation here
        pass

    def _normalise_newpage(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX newpage node."""
        # Implementation here
        pass

    def _normalise_color(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX color node."""
        # Implementation here
        pass

    def _normalise_box(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX box node."""
        # Implementation here
        pass

    def _normalise_column(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX column node."""
        # Implementation here
        pass

    def _normalise_other(self, node: TexNode) -> NormalisedNode:
        """Normalise a LaTeX other node."""
        return Other(
            name=node.name,
            original_content=str(node),
        )

class Denormaliser:
    def __init__(self, format_type: FormatType):
        self.format_type = format_type

        self.format: IFormat = FORMATS[format_type]()

    def denormalise(self, node: 'NormalisedNode') -> str:
        """
        Denormalise a node to its string representation

        Args:
            node: The node to denormalise

        Returns:
            String representation of the node
        """
        denormaliser_map = {
            Text: self._denormalise_text,
            Package: self._denormalise_package,
            DocumentClass: self._denormalise_document_class,
            Author: self._denormalise_author,
            Title: self._denormalise_title,
            Section: self._denormalise_section,
            Figure: self._denormalise_figure,
            MathFormula: self._denormalise_math_formula,
            Table: self._denormalise_table,
            Abstract: self._denormalise_abstract,
            Date: self._denormalise_date,
            Keywords: self._denormalise_keywords,
            Reference: self._denormalise_reference,
            Other: self._denormalise_other
        }

        node_type = type(node)
        if node_type in denormaliser_map:
            return denormaliser_map[node_type](node)

    def _denormalise_text(self, node: Text) -> str:
        return node.text

    def _denormalise_package(self, node: Package) -> str:
        return f"\\usepackage[{','.join(node.options)}]{{{','.join(node.names)}}}"

    def _denormalise_document_class(self, node: DocumentClass) -> str:
        return f"\\documentclass[{','.join(node.options)}]{{{node.type.value}}}"

    def _denormalise_author(self, node: Author) -> str:
        data: dict= node.model_dump(exclude_none=True)

        return Settings.get("author").render(**data)

    def _denormalise_title(self, node: Title) -> str:
        return (f"\\title{{{node.title}}}"
                + (f"\\\\{node.subtitle}" if node.subtitle else ""))

    def _denormalise_section(self, node: Section) -> str:
        return (f"\\{'sub' * (node.level - 1)}section"
                + f"{{{node.title}}}\n{node.content}")

    def _denormalise_figure(self, node: Figure) -> str:
        return (f"\\includegraphics"
                + (f"[width={node.width}]" if node.width else "")
                + f"{{{node.filename}}}")

    def _denormalise_math_formula(self, node: MathFormula) -> str:
        return (f"\\begin{{equation}}{node.formula}"
                + (f"\\label{{{node.label}}}" if node.label else "")
                + "\\end{equation}")

    def _denormalise_table(self, node: Table) -> str:
        rows = " \\\\\n".join(
            [
                " & ".join(
                    [
                        f"\\multicolumn{{{cell.colspan}}}{{c|}}{{{cell.content}}}"
                        if cell.colspan > 1
                        else f"\\multirow{{{cell.rowspan}}}{{*}}{{{cell.content}}}"
                        if cell.rowspan > 1
                        else str(cell.content)
                        for cell in row
                    ]
                )
                for row in node.rows
            ]
        )
        return (f"\\begin{{table}}[]\n"
                f"\\centering\n"
                + (f"\\caption{{{node.caption}}}\n" if node.caption else "")
                + (f"\\label{{{node.label}}}\n" if node.label else "")
                + f"\\begin{{tabular}}{{{"|".join(["l"] * len(node.rows[0]))}}}\n"
                + f"{rows}\n"
                + f"\\end{{tabular}}\n"
                + f"\\end{{table}}")

    def _denormalise_abstract(self, node: Abstract) -> str:
        return f"\\begin{{abstract}}{node.content}\\end{{abstract}}"

    def _denormalise_date(self, node: Date) -> str:
        return f"\\date{{{node.date}}}"

    def _denormalise_keywords(self, node: Keywords) -> str:
        return f"\\keywords{{{','.join(node.words)}}}"

    def _denormalise_reference(self, node: Reference) -> str:
        fields = "\n".join(
            [f"{key}={{{value}}}" for key, value in node.additional_fields.items()]
        )
        return (f"@{node.type}{{{node.key},\n"
                f"author={{{','.join(node.authors)}}},\n"
                f"title={{{node.title}}},\n"
                f"year={{{node.year}}},\n"
                + (f"journal={{{node.journal}}},\n" if node.journal else "")
                + (f"volume={{{node.volume}}},\n" if node.volume else "")
                + (f"number={{{node.number}}},\n" if node.number else "")
                + (f"pages={{{node.pages}}},\n" if node.pages else "")
                + (f"publisher={{{node.publisher}}},\n" if node.publisher else "")
                + (f"booktitle={{{node.booktitle}}},\n" if node.booktitle else "")
                + (f"doi={{{node.doi}}},\n" if node.doi else "")
                + (f"url={{{node.url}}},\n" if node.url else "")
                + fields
                + "}")

    def _denormalise_other(self, node: Other) -> str:
        return f"\\{node.name}"
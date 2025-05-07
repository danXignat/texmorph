import TexSoup as ts
from abc import ABC, abstractmethod
from typing import override, Union

from core.CIRTree import CIRTree
from models.types import FormatType, ElementType
from normalisation import Normaliser, Denormaliser
from models.normalisation import *

class Visitor(ABC):
    @abstractmethod
    def visit(self, node: Union[ts.TexNode, ts.TexSoup]):
        pass

    @abstractmethod
    def get(self):
        pass

class ASTVisitor(Visitor):
    def __init__(self, normaliser: Normaliser):
        self._normaliser    : Normaliser            = normaliser
        self._cir_tree      : CIRTree | None        = None
        self._curr_node     : NormalisedNode | None = None

    @override
    def visit(self, node: Union[ts.TexNode, ts.TexSoup]):
        match type(node.expr if hasattr(node, 'expr') else node):
            case ts.data.TexEnv:
                self._visit_env(node)

            case ts.data.TexNamedEnv:
                self._visit_named_env(node)

            case ts.data.TexUnNamedEnv:
                self._visit_unnamed_env(node)

            case ts.data.TexCmd:
                self._visit_cmd(node)

            case ts.data.Token:
                self._visit_token(node)

            case ts.data.TexMathModeEnv:
                self._visit_math_mode_env(node)

            case _:
                print(f"[WARNING] Unknown node type: {type(node)}")

    def _visit_env(self, node: ts.TexNode):
        """ Building cir tree"""
        doc_class   = self._normaliser.normalise(node.documentclass) if node.documentclass else None
        title       = self._normaliser.normalise(node.title)         if node.title else None
        abstract    = self._normaliser.normalise(node.abstract)      if node.abstract else None
        packages    = [self._normaliser.normalise(_node) for _node in node.find_all('usepackage')]
        authors     = [self._normaliser.normalise(_node) for _node in node.find_all('author')]

        self._cir_tree = CIRTree(
            doc_class=doc_class,
            packages=packages,
            authors=authors,
            title=title,
            abstract=abstract,
        )

        self.visit(node.document)

    def _visit_named_env(self, node: ts.TexNode):
        if node.name == 'document':
            self._cir_tree.root = self._normaliser.normalise(node)
            self._curr_node = self._cir_tree.root

            for child in node.contents:
                self.visit(child)
        else:
            normalised = self._normaliser.normalise(node)

            normalised.parent = self._curr_node
            self._curr_node.children.append(normalised)

            self._curr_node = normalised

    def _visit_cmd(self, node: ts.TexNode):
        normalised = self._normaliser.normalise(node)

        self._curr_node.children.append(normalised)

    def _visit_token(self, node: ts.TexNode):
        normalised = self._normaliser.normalise(node)

        self._curr_node.children.append(normalised)

    def _visit_math_mode_env(self, node: ts.TexNode):
        pass

    def _visit_unnamed_env(self, node: ts.TexNode):
        pass

    @override
    def get(self):
        return self._cir_tree


class CIRVisitor(Visitor):
    def __init__(self, denormaliser: Denormaliser, cir: CIRTree):
        self._cir_tree      : CIRTree       = cir
        self._denormaliser  : Denormaliser  = denormaliser
        self._contents      : list[str]     = self._build_preamble()
        # self._ast_tree      : ts.TexSoup | None = None
        # self._curr_node     : ts.TexNode | None = None

    @override
    def visit(self, node: NormalisedNode):
        if isinstance(node, Other) and node.name == "document":
            self._contents.append("\\begin{document}\n")

            for child in node.children:
                self.visit(child)

            self._contents.append("\\end{document}\n")
        else:
            self._contents.append(self._denormaliser.denormalise(node))

            for child in node.children:
                self.visit(child)

    @override
    def get(self):
        return "\n".join(self._contents)

    def _build_preamble(self) -> list[str]:
        preamble: list[str] = []

        if self._cir_tree.doc_class is not None:
            preamble.append(self._denormaliser.denormalise(self._cir_tree.doc_class))

        if self._cir_tree.title is not None:
            preamble.append(self._denormaliser.denormalise(self._cir_tree.title))

        if self._cir_tree.abstract is not None:
            preamble.append(self._denormaliser.denormalise(self._cir_tree.abstract))

        # preamble.extend([self._denormaliser.denormalise(p) for p in self._cir_tree.packages])
        preamble.extend([p.render() for p in self._denormaliser.format.packages])
        preamble.extend([self._denormaliser.denormalise(p) for p in self._cir_tree.authors])

        return preamble



if __name__ == "__main__":
    ast = ts.TexSoup(r"""
    \documentclass{article}
    
    \usepackage{amsmath}
    
    \begin{document}
    Cosmin
    \section{The section title}
    \begin{table}
    \centering
    \begin{tabular}{l|r}
    Item & Quantity \\\hline
    Widgets & 42 \\
    Gadgets & 13
    \end{tabular}
    \caption{\label{tab:widgets}An example table.}
    \end{table}
    \end{document}
    """)
    normaliser = Normaliser(format_type=FormatType.ARTICLE)
    denormaliser = Denormaliser(format_type=FormatType.ARTICLE)

    ast_visitor = ASTVisitor(normaliser=normaliser)
    ast_visitor.visit(ast)

    cir_visitor = CIRVisitor(denormaliser=denormaliser, cir=ast_visitor.get())
    cir_visitor.visit(ast_visitor.get().root)

    print(ast_visitor.get())
    print(cir_visitor.get())

    # from rag.extraction import RAGExtractor
    # from models.elements import Table
    #
    # extractor = RAGExtractor()
    #
    # model = extractor.extract(ElementType.TABLE, str(ast), Table)
    #
    # print(model)
    # print(model.cells)
    # print(Table.model_json_schema())


import TexSoup as ts

from core.visitation import ASTVisitor, CIRVisitor
from core.normalisation import Normaliser, Denormaliser

from models.types import FormatType

from utils.compile import compile_tex_from_string

def convert(tex: str, compile: bool=True, ) -> str:
    ast = ts.TexSoup(tex)

    normaliser = Normaliser(format_type=FormatType.ARTICLE)
    denormaliser = Denormaliser(format_type=FormatType.ARTICLE)

    ast_visitor = ASTVisitor(normaliser=normaliser)
    ast_visitor.visit(ast)

    cir_visitor = CIRVisitor(denormaliser=denormaliser, cir=ast_visitor.get())
    cir_visitor.visit(ast_visitor.get().root)

    tex: str = cir_visitor.get()

    if compile:
        compile_tex_from_string(tex)

    return tex

if __name__ == "__main__":
    convert(r"""
    \documentclass{article}
    
    \usepackage{amsmath}
    
    \begin{document}
    Cosmin
    \section{The section title}
    
    \end{document}
    """)
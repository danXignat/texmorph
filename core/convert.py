import TexSoup as ts

from core.visitation import ASTVisitor, CIRVisitor
from core.normalisation import Normaliser, Denormaliser

from models.types import FormatType
from utils.extraction import get_required
from utils.compile import compile_tex_from_string

def extract_format_type(soup: ts.TexSoup) -> FormatType:
    """ Extracts format type from tex soup """
    doc_class = soup.documentclass

    arg = get_required(doc_class)[-1]

    return FormatType(arg)

def requires_bibfile(soup: ts.TexSoup) -> bool:
    """ Checks if tex soup has bibtex """
    if soup.find('bibliography'):
        return True

    return False

def convert(tex: str, to_format: FormatType, compile: bool=True, ) -> str:
    """ Converts to specified format """
    ast     : ts.TexSoup = ts.TexSoup(tex)
    from_format  : FormatType = extract_format_type(ast)

    normaliser  : Normaliser = Normaliser(format_type=from_format)
    ast_visitor : ASTVisitor = ASTVisitor(normaliser=normaliser)
    ast_visitor.visit(ast)

    denormaliser: Denormaliser = Denormaliser(format_type=to_format)
    cir_visitor :CIRVisitor = CIRVisitor(denormaliser=denormaliser, cir=ast_visitor.get())
    cir_visitor.visit(ast_visitor.get().root)

    tex: str = cir_visitor.get()

    if compile:
        compile_tex_from_string(tex)

    return tex

if __name__ == "__main__":
    texes = [r"""
    \documentclass{article}
    
    \usepackage{amsmath}
    
    \begin{document}
    Cosmin
    \section{The section title}
    
    \begin{table}
    \centering
    \begin{tabular}{l|r}
    Item & Quantity \\
    Widgets & 42 \\
    Gadgets & 13
    \end{tabular}
    \caption{\label{tab:widgets}An example table.}
    \end{table}
    
    \end{document}
    """,
    r"""
    \documentclass{article}
    
    \author{Cosmin}
    
    \begin{document}
    
    \end{document}
    """]



    print(
        convert(texes[1], FormatType.IEEE, compile=False)
    )
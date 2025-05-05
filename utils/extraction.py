import TexSoup as ts

def get_title(node: ts.TexSoup) -> str | None:
    title = node.find('title')
    return title.string if title else None


def get_abstract(node: ts.TexSoup):
    return node.find('abstract').string


def get_sections(node: ts.TexSoup):
    return node.find_all('section')


def get_required(node: ts.TexNode) -> list[str]:
    return [
        field.string for field in node.args
        if isinstance(field, ts.data.BraceGroup)
    ]

def get_optionals(node: ts.TexNode) -> list[str]:
    return [
        field.string for field in node.args
        if isinstance(field, ts.data.BracketGroup)
    ]

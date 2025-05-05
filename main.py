from TexSoup import TexSoup
from pathlib import Path
import pprint

from core.CIRTree import IRTree

pp=pprint.PrettyPrinter(indent=2, width=80, compact=False)

TEST_FILE   : Path = Path('./data/TEST/test_file.tex')
IEEE_FILE   : Path = Path('./data/IEEE/conference_101719.tex')
SPRING_FILE : Path = Path('./data/SPRINGER/sn-article.tex')

def main():
    ir = IRTree(open(TEST_FILE).read())

    pp.pprint(ir.get_dict())

if __name__ == "__main__":
    main()
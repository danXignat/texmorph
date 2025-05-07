from TexSoup import TexSoup
from pathlib import Path
import pprint

TEST_FILE   : Path = Path('./data/TEST/test_file.tex')
IEEE_FILE   : Path = Path('./data/IEEE/conference_101719.tex')
SPRING_FILE : Path = Path('./data/SPRINGER/sn-article.tex')

def main():
    from utils.compile import compile_tex

    compile_tex(SPRING_FILE, use_bibtex=True)

if __name__ == "__main__":
    main()
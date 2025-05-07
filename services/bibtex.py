import bibtexparser as btp
from pathlib import Path

from models.normalisation import Reference

def load_bib(bib_path: Path | str) -> dict[str, str]:
    """Loads a BibTeX file and returns a dictionary of entries."""
    path = Path(bib_path)

    if not path.exists():
        raise FileNotFoundError(f"File {path} not found.")

    bib_file = open(path, "r")

    return btp.load(bib_file)

if __name__ == '__main__':
    bib = open("../data/TEST/sample.bib", "r")

    lib = btp.load(bib)

    refs = [Reference(**(entry | {"original_content": ""})) for entry in lib.entries]

    print(refs)



import bibtexparser as btp

from models.elements import Reference

if __name__ == '__main__':
    bib = open("../data/TEST/sample.bib", "r")

    lib = btp.load(bib)

    refs = [Reference(**(entry | {"original_content": ""})) for entry in lib.entries]

    print(refs)



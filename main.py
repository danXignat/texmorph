from core.Parser import Parser

import pprint
pp=pprint.PrettyPrinter(indent=2, width=80, compact=False)

test_file = 'data/TEST/test_file.tex'
ieee_file = 'data/IEEE/conference_101719.tex'

def main():
    parser = Parser()

    parser.parse(test_file)

    pp.pprint(parser.document_tree)


if __name__ == "__main__":
    main()
class DocumentModel:
    """Format-neutral document model"""

    def __init__(self, parser_output):
        self.metadata = {
            "title": "",
            "authors": [],
            "abstract": "",
            "keywords": [],
            "date": ""
        }
        self.sections = []
        self.references = []
        self.figures = []
        self.tables = []
        self.equations = []
        self.original_structure = parser_output

        self._build_from_parser(parser_output)

    def _build_from_parser(self, parser_output):
        """Convert parser output to structured document model"""
        # Extract metadata
        preamble = parser_output.get("preamble", {})
        if "title" in preamble:
            self.metadata["title"] = preamble["title"]

        if "author" in preamble:
            # Split multiple authors if necessary
            authors_text = preamble["author"]
            # Simple split by 'and' - more complex parsing might be needed
            authors = [author.strip() for author in authors_text.split(" and ")]
            self.metadata["authors"] = authors

        if "date" in preamble:
            self.metadata["date"] = preamble["date"]

        # Extract body content
        body = parser_output.get("body", {})

        # Extract sections
        self.sections = body.get("sections", [])

        # Extract figures
        self.figures = body.get("figures", [])

        # Extract tables
        self.tables = body.get("tables", [])

        # Extract equations
        self.equations = body.get("equations", [])

        # Extract bibliography
        bib_info = body.get("bibliography", {})
        self.references = {
            "style": bib_info.get("style", ""),
            "system": bib_info.get("system", "bibtex"),
            "sources": bib_info.get("sources", []),
            "citations": bib_info.get("citations", [])
        }

        # Try to extract abstract if available
        abstract_pattern = r'\\begin{abstract}(.*?)\\end{abstract}'
        abstract_match = re.search(abstract_pattern, parser_output.get("original", ""), re.DOTALL)
        if abstract_match:
            self.metadata["abstract"] = abstract_match.group(1).strip()

        # Try to extract keywords if available
        keywords_pattern = r'\\keywords{(.*?)}'
        keywords_match = re.search(keywords_pattern, parser_output.get("original", ""))
        if keywords_match:
            keywords = [kw.strip() for kw in keywords_match.group(1).split(',')]
            self.metadata["keywords"] = keywords


class FormatTransformer:
    """Base transformer class"""

    def __init__(self, document_model):
        self.document = document_model

    def transform(self):
        """Apply transformation rules"""
        raise NotImplementedError

    def _read_template(self, template_path):
        """Read a template file"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Template file not found: {template_path}")
            return ""

    def _copy_resources(self, source_dir, target_dir):
        """Copy resource files (images, bib files, etc.)"""
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Copy image files
        for ext in ['png', 'jpg', 'jpeg', 'pdf', 'eps']:
            for img_file in Path(source_dir).glob(f'*.{ext}'):
                shutil.copy(img_file, target_dir)

        # Copy bibliography files
        for bib_file in Path(source_dir).glob('*.bib'):
            shutil.copy(bib_file, target_dir)


class IEEETransformer(FormatTransformer):
    """Transform LaTeX document to IEEE format"""

    def transform(self):
        """Apply IEEE-specific transformations"""
        logger.info("Transforming to IEEE format")

        result = {
            "preamble": self._transform_preamble(),
            "body": self._transform_body(),
            "bibliography": self._transform_bibliography()
        }

        return result

    def _transform_preamble(self):
        """Convert preamble to IEEE format"""
        ieee_preamble = []

        # Add IEEE document class
        ieee_preamble.append(r'\documentclass[conference]{IEEEtran}')

        # Add standard IEEE packages
        ieee_preamble.extend([
            r'\usepackage{cite}',
            r'\usepackage{amsmath,amssymb,amsfonts}',
            r'\usepackage{algorithmic}',
            r'\usepackage{graphicx}',
            r'\usepackage{textcomp}',
            r'\usepackage{xcolor}'
        ])

        # Add additional packages that were in the original
        original_packages = self.document.original_structure.get("preamble", {}).get("packages", [])
        added_packages = set(
            ['cite', 'amsmath', 'amssymb', 'amsfonts', 'algorithmic', 'graphicx', 'textcomp', 'xcolor'])

        for package in original_packages:
            pkg_name = package.get("name", "")
            if pkg_name not in added_packages and pkg_name not in ['IEEEtran', 'ieeetran']:
                options = package.get("options", [])
                if options:
                    options_str = ','.join(options)
                    ieee_preamble.append(f'\\usepackage[{options_str}]{{{pkg_name}}}')
                else:
                    ieee_preamble.append(f'\\usepackage{{{pkg_name}}}')

        # Add title and author information
        if self.document.metadata.get("title"):
            ieee_preamble.append(f'\\title{{{self.document.metadata["title"]}}}')

        # Format authors for IEEE
        authors = self.document.metadata.get("authors", [])
        if authors:
            if len(authors) == 1:
                ieee_preamble.append(f'\\author{{{authors[0]}}}')
            else:
                # IEEE format typically uses \IEEEauthorblockN and \IEEEauthorblockA
                # for multiple authors, but simplified here
                authors_str = ' \\and '.join(authors)
                ieee_preamble.append(f'\\author{{{authors_str}}}')

        return '\n'.join(ieee_preamble)

    def _transform_body(self):
        """Transform document body to IEEE format"""
        ieee_body = []

        # Begin document
        ieee_body.append(r'\begin{document}')
        ieee_body.append(r'\maketitle')

        # Add abstract if available
        abstract = self.document.metadata.get("abstract")
        if abstract:
            ieee_body.append(r'\begin{abstract}')
            ieee_body.append(abstract)
            ieee_body.append(r'\end{abstract}')

        # Add keywords if available
        keywords = self.document.metadata.get("keywords")
        if keywords:
            keywords_str = ', '.join(keywords)
            ieee_body.append(r'\begin{IEEEkeywords}')
            ieee_body.append(keywords_str)
            ieee_body.append(r'\end{IEEEkeywords}')

        # Function to recursively add sections
        def add_sections(sections, level=0):
            for section in sections:
                section_type = section.get("type", "section")
                title = section.get("title", "")
                content = section.get("content", "")

                ieee_body.append(f'\\{section_type}{{{title}}}')

                # Add content (excluding nested sections)
                if content:
                    ieee_body.append(content)

                # Add subsections recursively
                subsections = section.get("subsections", [])
                if subsections:
                    add_sections(subsections, level + 1)

        # Add all sections
        add_sections(self.document.sections)

        # End document
        ieee_body.append(r'\end{document}')

        return '\n'.join(ieee_body)

    def _transform_bibliography(self):
        """Transform bibliography to IEEE format"""
        bib_system = self.document.references.get("system", "bibtex")
        bib_style = self.document.references.get("style", "")
        bib_sources = self.document.references.get("sources", [])

        if not bib_sources:
            return ""

        if bib_system == "biblatex":
            # Convert biblatex to BibTeX for IEEE
            bib_commands = [
                r'\bibliographystyle{IEEEtran}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]
        else:
            bib_commands = [
                r'\bibliographystyle{IEEEtran}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]

        return '\n'.join(bib_commands)


class SpringerNatureTransformer(FormatTransformer):
    """Transform LaTeX document to Springer Nature format"""

    def transform(self):
        """Apply Springer Nature-specific transformations"""
        logger.info("Transforming to Springer Nature format")

        result = {
            "preamble": self._transform_preamble(),
            "body": self._transform_body(),
            "bibliography": self._transform_bibliography()
        }

        return result

    def _transform_preamble(self):
        """Convert preamble to Springer Nature format"""
        springer_preamble = []

        # Add Springer document class
        springer_preamble.append(r'\documentclass[smallextended]{svjour3}')

        # Add standard Springer packages
        springer_preamble.extend([
            r'\usepackage{mathptmx}',
            r'\usepackage{amsmath}',
            r'\usepackage{graphicx}'
        ])

        # Add additional packages that were in the original
        original_packages = self.document.original_structure.get("preamble", {}).get("packages", [])
        added_packages = set(['mathptmx', 'amsmath', 'graphicx'])

        for package in original_packages:
            pkg_name = package.get("name", "")
            if pkg_name not in added_packages and pkg_name not in ['svjour3']:
                options = package.get("options", [])
                if options:
                    options_str = ','.join(options)
                    springer_preamble.append(f'\\usepackage[{options_str}]{{{pkg_name}}}')
                else:
                    springer_preamble.append(f'\\usepackage{{{pkg_name}}}')

        # Add Springer journal info (placeholder)
        springer_preamble.append(r'\journalname{Journal of Example}')

        # Add title and author information
        if self.document.metadata.get("title"):
            springer_preamble.append(f'\\title{{{self.document.metadata["title"]}}}')

        # Format authors for Springer Nature
        authors = self.document.metadata.get("authors", [])
        if authors:
            # Springer typically uses \author and \institute
            for i, author in enumerate(authors):
                springer_preamble.append(f'\\author{{{author}}}')
                # Add institute command (placeholder)
                springer_preamble.append(f'\\institute{{Institute {i + 1}}}')

        return '\n'.join(springer_preamble)

    def _transform_body(self):
        """Transform document body to Springer Nature format"""
        springer_body = []

        # Begin document
        springer_body.append(r'\begin{document}')
        springer_body.append(r'\maketitle')

        # Add abstract if available
        abstract = self.document.metadata.get("abstract")
        if abstract:
            springer_body.append(r'\begin{abstract}')
            springer_body.append(abstract)
            springer_body.append(r'\end{abstract}')

        # Add keywords if available
        keywords = self.document.metadata.get("keywords")
        if keywords:
            keywords_str = ' \\and '.join(keywords)
            springer_body.append(f'\\keywords{{{keywords_str}}}')

        # Function to recursively add sections
        def add_sections(sections, level=0):
            for section in sections:
                section_type = section.get("type", "section")
                title = section.get("title", "")
                content = section.get("content", "")

                springer_body.append(f'\\{section_type}{{{title}}}')

                # Add content (excluding nested sections)
                if content:
                    springer_body.append(content)

                # Add subsections recursively
                subsections = section.get("subsections", [])
                if subsections:
                    add_sections(subsections, level + 1)

        # Add all sections
        add_sections(self.document.sections)

        # End document
        springer_body.append(r'\end{document}')

        return '\n'.join(springer_body)

    def _transform_bibliography(self):
        """Transform bibliography to Springer Nature format"""
        bib_system = self.document.references.get("system", "bibtex")
        bib_style = self.document.references.get("style", "")
        bib_sources = self.document.references.get("sources", [])

        if not bib_sources:
            return ""

        if bib_system == "biblatex":
            # Convert biblatex to BibTeX for Springer
            bib_commands = [
                r'\bibliographystyle{spbasic}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]
        else:
            bib_commands = [
                r'\bibliographystyle{spbasic}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]

        return '\n'.join(bib_commands)


class FormatConverter:
    """Main converter class that orchestrates the conversion process"""

    def __init__(self, input_file=None, output_format=None, output_dir=None):
        self.input_file = input_file
        self.output_format = output_format.lower() if output_format else None
        self.output_dir = output_dir or os.path.join(os.path.dirname(input_file), 'converted')
        self.parser = None
        self.document_model = None
        self.transformer = None

    def convert(self):
        """Convert the document to the specified format"""
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # 1. Parse input file
        self._parse_document()

        # 2. Build document model
        self._build_document_model()

        # 3. Select and apply transformer
        self._transform_document()

        # 4. Write output file
        return self._write_output()

    def _parse_document(self):
        """Parse the input document"""
        logger.info(f"Parsing document: {self.input_file}")
        self.parser = LaTeXParser(os.path.dirname(self.input_file))

        try:
            return self.parser.parse(self.input_file)
        except Exception as e:
            logger.error(f"Error parsing document: {str(e)}")
            raise

    def _build_document_model(self):
        """Build the document model from parser output"""
        logger.info("Building document model")
        parser_output = self.parser.document_tree
        self.document_model = DocumentModel(parser_output)
        return self.document_model

    def _transform_document(self):
        """Transform the document to the specified format"""
        logger.info(f"Transforming document to {self.output_format} format")

        if self.output_format == 'ieee':
            self.transformer = IEEETransformer(self.document_model)
        elif self.output_format == 'springer' or self.output_format == 'nature':
            self.transformer = SpringerNatureTransformer(self.document_model)
        else:
            logger.error(f"Unsupported output format: {self.output_format}")
            raise ValueError(f"Unsupported output format: {self.output_format}")

        return self.transformer.transform()

    def _write_output(self):
        """Write the transformed document to the output file"""
        output_filename = os.path.join(
            self.output_dir,
            f"{os.path.splitext(os.path.basename(self.input_file))[0]}_{self.output_format}.tex"
        )

        logger.info(f"Writing output to {output_filename}")

        transformed = self.transformer.transform()

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                # Write preamble
                f.write(transformed['preamble'])
                f.write('\n\n')

                # Write body
                f.write(transformed['body'])
                f.write('\n\n')

                # Write bibliography
                if transformed['bibliography']:
                    f.write(transformed['bibliography'])

            # Copy necessary resources
            if os.path.dirname(self.input_file) != self.output_dir:
                self.transformer._copy_resources(
                    os.path.dirname(self.input_file),
                    self.output_dir
                )

            return output_filename
        except Exception as e:
            logger.error(f"Error writing output file: {str(e)}")
            raise


class ACMTransformer(FormatTransformer):
    """Transform LaTeX document to ACM format"""

    def transform(self):
        """Apply ACM-specific transformations"""
        logger.info("Transforming to ACM format")

        result = {
            "preamble": self._transform_preamble(),
            "body": self._transform_body(),
            "bibliography": self._transform_bibliography()
        }

        return result

    def _transform_preamble(self):
        """Convert preamble to ACM format"""
        acm_preamble = []

        # Add ACM document class
        acm_preamble.append(r'\documentclass[sigconf]{acmart}')

        # Add standard ACM packages
        acm_preamble.extend([
            r'\usepackage{booktabs}',  # For formal tables
            r'\usepackage{amsmath}'  # For math equations
        ])

        # Add additional packages that were in the original
        original_packages = self.document.original_structure.get("preamble", {}).get("packages", [])
        added_packages = set(['booktabs', 'amsmath'])

        for package in original_packages:
            pkg_name = package.get("name", "")
            if pkg_name not in added_packages and pkg_name not in ['acmart']:
                options = package.get("options", [])
                if options:
                    options_str = ','.join(options)
                    acm_preamble.append(f'\\usepackage[{options_str}]{{{pkg_name}}}')
                else:
                    acm_preamble.append(f'\\usepackage{{{pkg_name}}}')

        # Add ACM-specific metadata
        acm_preamble.extend([
            r'\acmConference[Conference acronym]{Conference name}{Conference date}{Conference location}',
            r'\acmYear{2025}',
            r'\setcopyright{acmcopyright}'
        ])

        # Add title and author information
        if self.document.metadata.get("title"):
            acm_preamble.append(f'\\title{{{self.document.metadata["title"]}}}')

        # Format authors for ACM
        authors = self.document.metadata.get("authors", [])
        if authors:
            for author in authors:
                # In real implementation, parse author names more carefully
                acm_preamble.append(f'\\author{{{author}}}')
                acm_preamble.append(r'\affiliation{')
                acm_preamble.append(r'  \institution{Author Institution}')
                acm_preamble.append(r'  \country{Country}')
                acm_preamble.append(r'}')

        return '\n'.join(acm_preamble)

    def _transform_body(self):
        """Transform document body to ACM format"""
        acm_body = []

        # Begin document
        acm_body.append(r'\begin{document}')
        acm_body.append(r'\maketitle')

        # Add abstract if available
        abstract = self.document.metadata.get("abstract")
        if abstract:
            acm_body.append(r'\begin{abstract}')
            acm_body.append(abstract)
            acm_body.append(r'\end{abstract}')

        # Add keywords if available (ACM uses \keywords command)
        keywords = self.document.metadata.get("keywords")
        if keywords:
            keywords_str = ', '.join(keywords)
            acm_body.append(f'\\keywords{{{keywords_str}}}')

        # Function to recursively add sections
        def add_sections(sections, level=0):
            for section in sections:
                section_type = section.get("type", "section")
                title = section.get("title", "")
                content = section.get("content", "")

                acm_body.append(f'\\{section_type}{{{title}}}')

                # Add content (excluding nested sections)
                if content:
                    acm_body.append(content)

                # Add subsections recursively
                subsections = section.get("subsections", [])
                if subsections:
                    add_sections(subsections, level + 1)

        # Add all sections
        add_sections(self.document.sections)

        # End document
        acm_body.append(r'\end{document}')

        return '\n'.join(acm_body)

    def _transform_bibliography(self):
        """Transform bibliography to ACM format"""
        bib_system = self.document.references.get("system", "bibtex")
        bib_style = self.document.references.get("style", "")
        bib_sources = self.document.references.get("sources", [])

        if not bib_sources:
            return ""

        # ACM now prefers biblatex, but can work with BibTeX
        if bib_system == "biblatex":
            bib_commands = [
                r'\bibliographystyle{ACM-Reference-Format}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]
        else:
            bib_commands = [
                r'\bibliographystyle{ACM-Reference-Format}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]

        return '\n'.join(bib_commands)


class ElsevierTransformer(FormatTransformer):
    """Transform LaTeX document to Elsevier format"""

    def transform(self):
        """Apply Elsevier-specific transformations"""
        logger.info("Transforming to Elsevier format")

        result = {
            "preamble": self._transform_preamble(),
            "body": self._transform_body(),
            "bibliography": self._transform_bibliography()
        }

        return result

    def _transform_preamble(self):
        """Convert preamble to Elsevier format"""
        elsevier_preamble = []

        # Add Elsevier document class
        elsevier_preamble.append(r'\documentclass[preprint,12pt]{elsarticle}')

        # Add standard Elsevier packages
        elsevier_preamble.extend([
            r'\usepackage{amssymb}',
            r'\usepackage{amsmath}',
            r'\usepackage{graphicx}'
        ])

        # Add additional packages that were in the original
        original_packages = self.document.original_structure.get("preamble", {}).get("packages", [])
        added_packages = set(['amssymb', 'amsmath', 'graphicx'])

        for package in original_packages:
            pkg_name = package.get("name", "")
            if pkg_name not in added_packages and pkg_name not in ['elsarticle']:
                options = package.get("options", [])
                if options:
                    options_str = ','.join(options)
                    elsevier_preamble.append(f'\\usepackage[{options_str}]{{{pkg_name}}}')
                else:
                    elsevier_preamble.append(f'\\usepackage{{{pkg_name}}}')

        # Add Elsevier journal info (placeholder)
        elsevier_preamble.append(r'\journal{Journal of Example}')

        # Add title
        if self.document.metadata.get("title"):
            elsevier_preamble.append(f'\\title{{{self.document.metadata["title"]}}}')

        # Format authors for Elsevier
        authors = self.document.metadata.get("authors", [])
        if authors:
            elsevier_preamble.append(r'\begin{frontmatter}')

            for i, author in enumerate(authors):
                elsevier_preamble.append(f'\\author{{{author}}}')
                elsevier_preamble.append(f'\\address{{Address {i + 1}, Department, Institution}}')
                elsevier_preamble.append(f'\\ead{{email{i + 1}@example.com}}')

            elsevier_preamble.append(r'\end{frontmatter}')

        return '\n'.join(elsevier_preamble)

    def _transform_body(self):
        """Transform document body to Elsevier format"""
        elsevier_body = []

        # Begin document
        elsevier_body.append(r'\begin{document}')
        elsevier_body.append(r'\begin{frontmatter}')

        # Add title and authors if not in preamble
        if self.document.metadata.get("title") and "\\begin{frontmatter}" not in self._transform_preamble():
            elsevier_body.append(f'\\title{{{self.document.metadata["title"]}}}')

            # Format authors for Elsevier
            authors = self.document.metadata.get("authors", [])
            if authors:
                for i, author in enumerate(authors):
                    elsevier_body.append(f'\\author{{{author}}}')
                    elsevier_body.append(f'\\address{{Address {i + 1}, Department, Institution}}')
                    elsevier_body.append(f'\\ead{{email{i + 1}@example.com}}')

        # Add abstract if available
        abstract = self.document.metadata.get("abstract")
        if abstract:
            elsevier_body.append(r'\begin{abstract}')
            elsevier_body.append(abstract)
            elsevier_body.append(r'\end{abstract}')

        # Add keywords if available
        keywords = self.document.metadata.get("keywords")
        if keywords:
            keywords_str = ', '.join(keywords)
            elsevier_body.append(r'\begin{keyword}')
            elsevier_body.append(keywords_str)
            elsevier_body.append(r'\end{keyword}')

        elsevier_body.append(r'\end{frontmatter}')

        # Function to recursively add sections
        def add_sections(sections, level=0):
            for section in sections:
                section_type = section.get("type", "section")
                title = section.get("title", "")
                content = section.get("content", "")

                elsevier_body.append(f'\\{section_type}{{{title}}}')

                # Add content (excluding nested sections)
                if content:
                    elsevier_body.append(content)

                # Add subsections recursively
                subsections = section.get("subsections", [])
                if subsections:
                    add_sections(subsections, level + 1)

        # Add all sections
        add_sections(self.document.sections)

        # End document
        elsevier_body.append(r'\end{document}')

        return '\n'.join(elsevier_body)

    def _transform_bibliography(self):
        """Transform bibliography to Elsevier format"""
        bib_system = self.document.references.get("system", "bibtex")
        bib_style = self.document.references.get("style", "")
        bib_sources = self.document.references.get("sources", [])

        if not bib_sources:
            return ""

        # Elsevier uses natbib by default
        if bib_system == "biblatex":
            # Convert biblatex to natbib
            bib_commands = [
                r'\bibliographystyle{elsarticle-num}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]
        else:
            bib_commands = [
                r'\bibliographystyle{elsarticle-num}',
                f'\\bibliography{{{",".join(bib_sources)}}}'
            ]

        return '\n'.join(bib_commands)

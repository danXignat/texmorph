import re
import logging
from TexSoup import TexSoup
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('parser')

class Parser:
    """Parser component using TeXSoup to convert LaTeX into structured representation"""
    def __init__(self, base_path='.'):
        self.document_tree = {}
        self.macros = {}
        self.base_path = Path(base_path)

    def parse(self, tex_file_path):
        """Parse LaTeX content into structured document tree"""
        logger.info(f"Starting LaTeX parsing of {tex_file_path}")

        tex_path = Path(tex_file_path)
        if not tex_path.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_file_path}")

        with open(tex_path, 'r', encoding='utf-8') as f:
            tex_content: str = f.read()

        self.document_tree["original"] = tex_content

        # Handle includes and imports first
        expanded_content = self._resolve_includes(tex_content, tex_path.parent)

        # Parse with TeXSoup
        try:
            soup = TexSoup(expanded_content)
            logger.info("Successfully parsed LaTeX with TeXSoup")
        except Exception as e:
            logger.error(f"TeXSoup parsing error: {str(e)}")
            # Fallback to more forgiving parsing if TeXSoup fails
            logger.info("Attempting fallback parsing method")
            return self._fallback_parse(expanded_content)

        # Extract document structure
        self.document_tree.update(self._extract_document_structure(soup))

        # Extract custom macros
        self.macros = self._extract_macros(soup)

        logger.info("LaTeX parsing completed")
        return self.document_tree

    def _resolve_includes(self, content, base_dir):
        """Handle input and include statements recursively"""
        logger.info("Resolving includes and inputs")

        def replace_include(match):
            include_file = match.group(1).strip()
            # Add .tex extension if not present
            if not include_file.endswith('.tex'):
                include_file += '.tex'

            include_path = base_dir / include_file
            try:
                with open(include_path, 'r', encoding='utf-8') as file:
                    logger.info(f"Including file: {include_path}")
                    included_content = file.read()
                    # Recursively resolve includes in the included file
                    return self._resolve_includes(included_content, include_path.parent)
            except FileNotFoundError:
                logger.warning(f"Could not find include file: {include_path}")
                return f"% MISSING INCLUDE: {include_file}"

        # Handle \input{file}
        content = re.sub(r'\\input\{([^}]+)\}', replace_include, content)

        # Handle \include{file}
        content = re.sub(r'\\include\{([^}]+)\}', replace_include, content)

        return content

    def _extract_document_structure(self, soup):
        """Extract the document structure using TeXSoup"""
        structure = {}

        # Extract preamble information
        structure["preamble"] = self._extract_preamble(soup)

        # Extract body content
        structure["body"] = self._extract_body(soup)

        return structure

    def _extract_preamble(self, soup):
        """Extract document class, packages and other preamble info"""
        preamble = {}

        # Extract document class
        doc_class = soup.find('documentclass')
        if doc_class:
            preamble["document_class"] = {
                "name": doc_class.name,
                "options": doc_class.args[0].string.split(",") if len(doc_class.args) > 1 else [],
                "class": doc_class.args[-1].string,
            }

        # Extract packages
        packages = []
        for pkg in soup.find_all('usepackage'):
            packages.append({
                "name": pkg.name,
                "options": pkg.args[0].string.split(",") if len(pkg.args) > 1 else [],
                "class": pkg.args[-1].string,
            })
        preamble["packages"] = packages

        # Extract title, author, date
        if soup.find('title'):
            preamble["title"] = str(soup.find('title').string)

        if soup.find('author'):
            preamble["author"] = str(soup.find('author').string)

        if soup.find('date'):
            preamble["date"] = str(soup.find('date').string)

        return preamble

    def _extract_body(self, soup):
        """Extract the document body structure"""
        body = {}

        # Get the document environment
        doc_env = soup.find('document')
        if not doc_env:
            logger.warning("No document environment found")
            return body

        # Extract sections
        body["sections"] = self._extract_sections(doc_env)

        # Extract figures
        body["figures"] = self._extract_environments(doc_env, "figure")

        # Extract tables
        body["tables"] = self._extract_environments(doc_env, "table")

        # Extract equations
        body["equations"] = self._extract_equations(doc_env)

        # Extract bibliography information
        body["bibliography"] = self._extract_bibliography(soup)

        return body

    def _extract_sections(self, doc_env):
        """Extract hierarchical section structure"""
        sections = []

        # Define section types in hierarchical order
        section_types = [
            "chapter",
            "section",
            "subsection",
            "subsubsection",
            "paragraph",
            "subparagraph"
        ]

        # Helper function to process sections recursively
        def process_section(node, level=0):
            if level >= len(section_types):
                return None

            section_type = section_types[level]
            result = []

            # Find all sections at this level
            for section in node.find_all(section_type):
                section_data = {
                    "type": section_type,
                    "title": str(section.string),
                    "level": level,
                    "content": self._extract_text_content(section),
                    "subsections": process_section(section, level + 1) or []
                }

                # Look for labels associated with this section
                label = section.find('label')
                if label:
                    section_data["label"] = str(label.string)

                result.append(section_data)

            return result if result else None

        # Start processing from the document level
        top_level_sections = []
        for section_type in section_types:
            for section in doc_env.find_all(section_type):
                level = section_types.index(section_type)
                section_data = {
                    "type": section_type,
                    "title": str(section.string),
                    "level": level,
                    "content": self._extract_text_content(section),
                    "subsections": process_section(section, level + 1) or []
                }

                # Look for labels associated with this section
                label = section.find('label')
                if label:
                    section_data["label"] = str(label.string)

                top_level_sections.append(section_data)

        return top_level_sections

    def _extract_text_content(self, node):
        """Extract the text content from a node, excluding nested sections"""
        # Skip section commands within this node
        section_types = ["chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph"]

        content = []
        for child in node.contents:
            # Skip any nested section commands
            if hasattr(child, 'name') and child.name in section_types:
                continue

            # Add text content
            content.append(str(child))

        return ''.join(content)

    def _extract_environments(self, doc_env, env_type):
        """Extract environments like figures, tables, etc."""
        environments = []

        for env in doc_env.find_all(env_type):
            env_data = {
                "type": env_type,
                "starred": env.name.endswith('*'),
                "content": str(env)
            }

            # Extract caption if present
            caption = env.find('caption')
            if caption:
                env_data["caption"] = str(caption.string)

                # Check for optional short caption
                if caption.args:
                    env_data["short_caption"] = str(caption.args[0])

            # Extract label if present
            label = env.find('label')
            if label:
                env_data["label"] = str(label.string)

            # Extract positioning
            if env.args:
                env_data["position"] = str(env.args[0])

            environments.append(env_data)

        return environments

    def _extract_equations(self, doc_env):
        """Extract equation environments and standalone equations"""
        equations = []

        # Extract equation environments
        equation_envs = ["equation", "align", "gather", "multline"]

        for env_type in equation_envs:
            for env in doc_env.find_all(env_type):
                eq_data = {
                    "type": env_type,
                    "starred": env.name.endswith('*'),
                    "content": str(env.string)
                }

                # Extract label if present
                label = env.find('label')
                if label:
                    eq_data["label"] = str(label.string)

                equations.append(eq_data)

        # NOTE: Standalone equations like $...$ and $$...$$ are more challenging
        # with TeXSoup and may require additional regex handling

        return equations

    def _extract_bibliography(self, soup):
        """Extract bibliography information"""
        bib_info = {}

        # Check for \bibliography command
        bib_cmd = soup.find('bibliography')
        if bib_cmd:
            bib_info["sources"] = [src.strip() for src in str(bib_cmd.string).split(',')]

        # Check for \bibliographystyle command
        style_cmd = soup.find('bibliographystyle')
        if style_cmd:
            bib_info["style"] = str(style_cmd.string)

        # Check for biblatex
        biblatex_pkg = None
        for pkg in soup.find_all('usepackage'):
            if pkg.name == 'biblatex':
                biblatex_pkg = pkg
                break

        if biblatex_pkg:
            bib_info["system"] = "biblatex"

            # Extract biblatex options
            if biblatex_pkg.args:
                bib_info["options"] = [opt.strip() for opt in str(biblatex_pkg.args[0]).split(',')]
        else:
            bib_info["system"] = "bibtex"

        # Extract citations (this is challenging with TeXSoup and might require regex)
        citations = set()
        cite_cmds = ['cite', 'citep', 'citet', 'parencite', 'textcite', 'autocite']

        for cmd in cite_cmds:
            for cite in soup.find_all(cmd):
                if cite.string:
                    for key in str(cite.string).split(','):
                        citations.add(key.strip())

        bib_info["citations"] = list(citations)

        return bib_info

    def _extract_macros(self, soup):
        """Extract custom macros and definitions"""
        macros = {}

        # Extract \newcommand definitions
        for cmd in soup.find_all('newcommand'):
            if len(cmd.args) >= 2:
                cmd_name = str(cmd.args[0])
                cmd_name = cmd_name.strip('\\{}')

                # Check if there's a number of arguments specified
                num_args = 0
                definition = str(cmd.args[-1])

                if len(cmd.args) >= 3:
                    try:
                        num_args = int(str(cmd.args[1]))
                    except ValueError:
                        pass

                macros[cmd_name] = {
                    "args": num_args,
                    "definition": definition
                }

        # Extract \def definitions (more challenging with TeXSoup)
        # This would require more specialized handling

        return macros

    def _fallback_parse(self, content):
        """Fallback parsing method if TeXSoup fails"""
        logger.info("Using fallback parsing method")

        # Create a basic structure through regex parsing
        structure = {
            "preamble": {},
            "body": {},
            "original": content
        }

        # Extract document class
        doc_class_match = re.search(r'\\documentclass(?:\[([^]]*)\])?\{([^}]+)\}', content)
        if doc_class_match:
            options = doc_class_match.group(1)
            doc_class = doc_class_match.group(2)

            structure["preamble"]["document_class"] = {
                "name": doc_class,
                "options": options.split(',') if options else []
            }

        # Extract packages
        package_pattern = r'\\usepackage(?:\[([^]]*)\])?\{([^}]+)\}'
        packages = []

        for match in re.finditer(package_pattern, content):
            options = match.group(1)
            package = match.group(2)

            packages.append({
                "name": package,
                "options": options.split(',') if options else []
            })

        structure["preamble"]["packages"] = packages

        # Basic extraction of section structure
        structure["body"]["sections"] = self._fallback_extract_sections(content)

        return structure

    def _fallback_extract_sections(self, content):
        """Fallback method to extract sections using regex"""
        sections = []

        # Define section types in hierarchical order
        section_types = [
            "chapter",
            "section",
            "subsection",
            "subsubsection",
            "paragraph",
            "subparagraph"
        ]

        # Create regex pattern for all section types
        section_pattern = '|'.join([f'\\\\{s}' for s in section_types])
        pattern = f'({section_pattern})\\*?\\{{([^}}]+)\\}}'

        for match in re.finditer(pattern, content):
            section_type = match.group(1).strip('\\')
            title = match.group(2)
            level = section_types.index(section_type)

            sections.append({
                "type": section_type,
                "title": title,
                "level": level,
                "content": "",  # Simplified - no content extraction in fallback
                "subsections": []
            })

        return sections
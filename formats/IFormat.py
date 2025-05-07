from models.format import CommandFormat, EnvironmentFormat, LatexFormat
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from models.types import FormatType
from config.settings import Settings

class IFormat(ABC):
    """Base class for document formats"""
    def __init__(self):
        self._init_settings()
        self._init_commands()
        self._init_environments()
        self._init_packages()

    @abstractmethod
    def _init_settings(self):
        """Initialize format-specific settings"""
        pass

    def _init_commands(self):
        """Initialize format-specific commands"""
        pass

    def _init_environments(self):
        """Initialize format-specific environments"""
        pass

    def _init_packages(self):
        """Initialize required packages"""
        pass

    def __del__(self):
        Settings.reset()

class IEEEFormat(IFormat):
    """IEEE conference format settings"""
    def __init__(self):
        super().__init__()

        self.packages = self._init_packages()

    def _init_settings(self):
        Settings.set("documentclass").options = ["conference"]
        Settings.set("documentclass").arguments = ["IEEEtran"]

        Settings.set("title").template = "\\{name}{{title}}}"
        Settings.set("author").template = "\\{_name}{{\\IEEEauthorblockN{{{name}}}\\IEEEauthorblockA{{{affiliation}}}}}"

        Settings.set("section").template = "\\{name}{{{content}}}"
        Settings.set("subsection").template = "\\{name}{{{content}}}"

        Settings.set("cite").template = "\\{name}{{{key}}}"

        Settings.set("table").options = ["htbp"]

        Settings.set("figure").options = ["htbp"]

    def _init_commands(self):
        # IEEE specific commands
        try:
            # IEEEkeywords command
            Settings.add_command(CommandFormat(
                name="IEEEkeywords",
                template="\\{name}{{{keywords}}}"
            ))

            # PARstart command for first paragraph
            Settings.add_command(CommandFormat(
                name="PARstart",
                template="\\{name}{{{first_letter}}}{{{rest_word}}}"
            ))

            # IEEEpeerreviewmaketitle command
            Settings.add_command(CommandFormat(
                name="IEEEpeerreviewmaketitle",
                template="\\{name}"
            ))
        except ValueError:
            # Command might already exist
            pass

    def _init_environments(self):
        # IEEE specific environments
        try:
            # IEEEkeywords environment
            Settings.add_environment(EnvironmentFormat(
                name="IEEEbiography",
                template="\\begin{{{name}}}[{photo}]{{{author}}}\\n{content}\\end{{{name}}}"
            ))

            # IEEEproof environment (alternative to standard proof)
            Settings.add_environment(EnvironmentFormat(
                name="IEEEproof",
                template="\\begin{{{name}}}[{theorem_name}]\\n{content}\\end{{{name}}}"
            ))
        except ValueError:
            # Environment might already exist
            pass

    def _init_packages(self) -> list[CommandFormat]:
        ieee_packages = [
            "cite",        # Enhanced citation capabilities
            "amsmath",     # Advanced math formatting
            "algorithmic", # For algorithm presentation
            "graphicx",    # For figure inclusion
            "textcomp",    # For special text symbols
            "amssymb",     # Additional math symbols
            "xcolor",      # Color support
        ]

        return [
            CommandFormat(name="usepackage", arguments=[p]) for p in ieee_packages
        ]

class SNFormat(IFormat):
    """Springer Nature format settings (LNCS)"""
    def __init__(self):
        super().__init__()

        self.packages = self._init_packages()

    def _init_settings(self):
        # Document class with llncs
        Settings.set("documentclass").options = []
        Settings.set("documentclass").arguments = ["llncs"]

        # Title and author settings
        Settings.set("title").template = "\\{name}{{{title}}}"
        Settings.set("author").template = "\\{name}{{{author}}}"

        # Section formatting - Springer formats use custom settings
        Settings.set("section").template = "\\{name}{{{content}}}"
        Settings.set("subsection").template = "\\{name}{{{content}}}"

        # Reference settings
        Settings.set("cite").template = "\\{name}{{{key}}}"

        # Table format
        Settings.set("table").options = ["t"]  # Typically top-aligned in Springer

        # Figure format
        Settings.set("figure").options = ["t"]  # Typically top-aligned in Springer

    def _init_commands(self):
        # Springer Nature specific commands
        try:
            # Institute command for affiliations
            Settings.add_command(CommandFormat(
                name="institute",
                template="\\{name}{{{affiliation}}}"
            ))

            # Keywords command
            Settings.add_command(CommandFormat(
                name="keywords",
                template="\\{name}{{{keywords}}}"
            ))

            # Thanks command for acknowledgments
            Settings.add_command(CommandFormat(
                name="thanks",
                template="\\{name}{{{acknowledgment}}}"
            ))

            # email command
            Settings.add_command(CommandFormat(
                name="email",
                template="\\{name}{{{address}}}"
            ))

            # titlerunning command for header
            Settings.add_command(CommandFormat(
                name="titlerunning",
                template="\\{name}{{{short_title}}}"
            ))

            # authorrunning command for header
            Settings.add_command(CommandFormat(
                name="authorrunning",
                template="\\{name}{{{short_authors}}}"
            ))
        except ValueError:
            # Command might already exist
            pass

    def _init_environments(self):
        # Springer Nature specific environments
        try:
            Settings.add_environment(EnvironmentFormat(
                name="abstract",
                template="\\begin{{{name}}}\\n{content}\\end{{{name}}}"
            ))

            Settings.add_environment(EnvironmentFormat(
                name="svmult",
                template="\\begin{{{name}}}\\n{content}\\end{{{name}}}"
            ))
        except ValueError:
            pass

    def _init_packages(self) -> list[CommandFormat]:
        sn_packages = [
            "graphicx",    # For figure inclusion
            "amsmath",     # Advanced math formatting
            "amssymb",     # Additional math symbols
            "mathptmx",    # Times font
            "hyperref",    # For hyperlinks
            "url",         # For formatting URLs
            "algorithmic", # For algorithm presentation
            "algorithm",   # For algorithm environments
            "booktabs",
        ]

        return [
            CommandFormat(name="usepackage", arguments=[p]) for p in sn_packages
        ]

FORMATS = {
    FormatType.IEEE: IEEEFormat,
    FormatType.SPRINGER: SNFormat
}
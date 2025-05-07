from models.format import CommandFormat, EnvironmentFormat, LatexFormat

class Settings:
    default_commands: list[CommandFormat] = [
        # Document structure
        CommandFormat(name="documentclass"),
        CommandFormat(name="title"),
        CommandFormat(name="author"),
        CommandFormat(name="date"),
        CommandFormat(name="maketitle"),
        CommandFormat(name="tableofcontents"),

        # Sectioning
        CommandFormat(name="part"),
        CommandFormat(name="chapter"),
        CommandFormat(name="section"),
        CommandFormat(name="subsection"),
        CommandFormat(name="subsubsection"),
        CommandFormat(name="paragraph"),
        CommandFormat(name="subparagraph"),

        # Text formatting
        CommandFormat(name="textbf"),
        CommandFormat(name="textit"),
        CommandFormat(name="texttt"),
        CommandFormat(name="textsc"),
        CommandFormat(name="underline"),
        CommandFormat(name="emph"),

        # Font size
        CommandFormat(name="tiny"),
        CommandFormat(name="scriptsize"),
        CommandFormat(name="footnotesize"),
        CommandFormat(name="small"),
        CommandFormat(name="normalsize"),
        CommandFormat(name="large"),
        CommandFormat(name="Large"),
        CommandFormat(name="LARGE"),
        CommandFormat(name="huge"),
        CommandFormat(name="Huge"),

        # Lists
        CommandFormat(name="item"),

        # References
        CommandFormat(name="label"),
        CommandFormat(name="ref"),
        CommandFormat(name="pageref"),
        CommandFormat(name="cite"),

        # Footnotes
        CommandFormat(name="footnote"),

        # Math
        CommandFormat(name="sqrt"),
        CommandFormat(name="frac"),
        CommandFormat(name="sum"),
        CommandFormat(name="int"),
        CommandFormat(name="prod"),
        CommandFormat(name="lim"),

        # Graphics
        CommandFormat(name="includegraphics"),

        # Tables
        CommandFormat(name="hline"),
        CommandFormat(name="multicolumn"),

        # Spacing
        CommandFormat(name="hspace"),
        CommandFormat(name="vspace"),
        CommandFormat(name="newpage"),
        CommandFormat(name="clearpage"),

        # Bibliography
        CommandFormat(name="bibliography"),
        CommandFormat(name="bibliographystyle"),

        # Miscellaneous
        CommandFormat(name="usepackage"),
        CommandFormat(name="input"),
        CommandFormat(name="include"),
        # Special case - removed custom template and arguments
        CommandFormat(name="newcommand"),
    ]

    default_environments: list[EnvironmentFormat] = [
        # Document
        EnvironmentFormat(name="document"),

        # Text alignment
        EnvironmentFormat(name="center"),
        EnvironmentFormat(name="flushleft"),
        EnvironmentFormat(name="flushright"),

        # Lists
        EnvironmentFormat(name="itemize"),
        EnvironmentFormat(name="enumerate"),
        EnvironmentFormat(name="description"),

        # Math
        EnvironmentFormat(name="math"),
        EnvironmentFormat(name="displaymath"),
        EnvironmentFormat(name="equation"),
        EnvironmentFormat(name="align"),
        EnvironmentFormat(name="gather"),
        EnvironmentFormat(name="multline"),
        EnvironmentFormat(name="array"),
        EnvironmentFormat(name="matrix"),
        EnvironmentFormat(name="pmatrix"),
        EnvironmentFormat(name="bmatrix"),
        EnvironmentFormat(name="vmatrix"),

        # Tables
        EnvironmentFormat(name="tabular"),
        EnvironmentFormat(name="table"),

        # Figures
        EnvironmentFormat(name="figure"),

        # Verbatim
        EnvironmentFormat(name="verbatim"),
        EnvironmentFormat(name="lstlisting"),
        EnvironmentFormat(name="minted"),

        # Theorem-like
        EnvironmentFormat(name="theorem"),
        EnvironmentFormat(name="proof"),
        EnvironmentFormat(name="lemma"),
        EnvironmentFormat(name="definition"),
        EnvironmentFormat(name="example"),

        # Quotations
        EnvironmentFormat(name="quote"),
        EnvironmentFormat(name="quotation"),

        # Bibliography
        EnvironmentFormat(name="thebibliography"),

        # Abstract
        EnvironmentFormat(name="abstract"),

        # Custom
        EnvironmentFormat(name="minipage"),
    ]

    special_commands = []
    special_environments = []

    _items = {i.name: i for i in default_commands + default_environments}

    @classmethod
    def get(cls, latex: str) -> LatexFormat:
        return cls._items[latex].model_copy()

    @classmethod
    def set(cls, latex: str) -> LatexFormat:
        return cls._items[latex]

    @classmethod
    def reset(cls) -> None:
        for v in cls._items.values():
            v.reset()
    @classmethod
    def add_command(cls, command: CommandFormat) -> None:
        if command.name in cls._items:
            raise ValueError(f"Command {command} already exists")

        cls.special_commands.append(command)
        cls._items[command.name] = command

    @classmethod
    def add_environment(cls, environment: EnvironmentFormat) -> None:
        if environment.name in cls._items:
            raise ValueError(f"Environ {environment} already exists")

        cls.special_environments.append(environment)
        cls._items[environment.name] = environment

if __name__ == "__main__":
    ieee_packages = [
        "cite",        # Enhanced citation capabilities
        "amsmath",     # Advanced math formatting
        "algorithmic", # For algorithm presentation
        "graphicx",    # For figure inclusion
        "textcomp",    # For special text symbols
        "amssymb",     # Additional math symbols
        "xcolor",      # Color support
    ]

    ls = [
        CommandFormat(name="usepackage", arguments=[p]) for p in ieee_packages
    ]

    for v in ls:
        print(v.render())




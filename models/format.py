from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from collections import defaultdict
from abc import abstractmethod

class LatexFormat(BaseModel):
    """Base class for LaTeX formats."""
    name: str
    template: str = ""

    @abstractmethod
    def render(self, **kwargs) -> str:
        """Render the LaTeX format using the template."""
        raise NotImplementedError(
            "Subclasses of LatexFormat must implement the render method.")

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError(
            "Subclasses of LatexFormat must implement the reseter method."
        )

class CommandFormat(LatexFormat):
    """Class for LaTeX commands."""
    arguments : list[str] = Field(default_factory=list)
    options   : list[str] = Field(default_factory=list)
    template  : str = "\\{_name}{arguments}"

    def render(self, *args, **kwargs) -> str:
        """Render the LaTeX command."""
        args_str = ""
        if self.options:
            options_list = [v for v in self.options]
            args_str += f"[{','.join(options_list)}]"

        if self.arguments:
            for arg in self.arguments:
                args_str += f"{{{arg}}}"

        if args:
            for arg in args:
                args_str += f"{{{arg}}}"

        df_dict = defaultdict(lambda: "", kwargs)
        return self.template.format(_name=self.name, arguments=args_str, **df_dict)

    def reset(self) -> None:
        self.arguments = []
        self.options = []

class EnvironmentFormat(LatexFormat):
    """Class for LaTeX environments."""
    children: list[Union['EnvironmentFormat', CommandFormat, str]] = Field(default_factory=list)
    options: list[str] = Field(default_factory=list)
    template: str = "\\begin{{{name}}}{options}\n{content}\\end{{{name}}}"

    def add_child(self, child: Union['EnvironmentFormat', CommandFormat, str]) -> None:
        """Add a child to the environment."""
        self.children.append(child)

    def render(self, *args, **kwargs) -> str:
        """Render the LaTeX environment with its children."""
        options_str = ""
        if self.options:
            options_list = [v for v in self.options]
            options_str = f"[{','.join(options_list)}]"

        children_content = ""
        for child in self.children:
            if isinstance(child, (EnvironmentFormat, CommandFormat)):
                children_content += child.render(**kwargs) + "\n"
            else:
                children_content += f"{child}\n"

        return self.template.format(
            name=self.name,
            options=options_str,
            content=children_content,
            **kwargs
        )

    def reset(self) -> None:
        self.children = []
        self.options = []
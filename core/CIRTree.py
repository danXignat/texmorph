from pydantic import BaseModel
from typing import Any

from models.normalisation import *


class CIRTree(BaseModel):
    doc_class: DocumentClass | None = None
    packages: list[Package] = Field(default_factory=list)
    authors: list[Author] = Field(default_factory=list)

    title: Title | None = None
    abstract: Abstract | None = None

    other: NormalisedNode | None = None

    root: NormalisedNode | None = None

    def __str__(self):
        """Returns a readable string representation of the CIRTree object."""
        root_str = f"\n    {str(self.root).replace(chr(10), chr(10) + '    ')}" if self.root else None
        other_str = f"\n    {str(self.other).replace(chr(10), chr(10) + '    ')}" if self.other else None

        authors_str = f"[{len(self.authors)} authors]" if self.authors else "[]"
        packages_str = f"[{len(self.packages)} packages]" if self.packages else "[]"

        return (
            f"CIRTree(\n"
            f"    doc_class={self.doc_class},\n"
            f"    packages={packages_str},\n"
            f"    authors={authors_str},\n"
            f"    title={self.title},\n"
            f"    abstract={self.abstract},\n"
            f"    other={other_str},\n"
            f"    root={root_str}\n"
            f")"
        )

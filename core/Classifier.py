from TexSoup import TexNode

from models.types import DocumentClassType, ElementType
from core.mapping import DEFAULT_MAPPING, IEEE_MAPPING, SPRINGER_MAPPING

class Classifier:
    def __init__(self, class_type: DocumentClassType):
        self.class_type = class_type

        match class_type:
            case DocumentClassType.ARTICLE:
                pass
            case DocumentClassType.IEEE:
                self.special_mapper: list[tuple] = IEEE_MAPPING
            case DocumentClassType.SPRINGER:
                self.special_mapper: list[tuple] = SPRINGER_MAPPING
            case _:
                raise ValueError(f"Unsupported document class type: {class_type}")

    def classify(self, node: TexNode) -> ElementType:
        name: str = node.name.string

        mapped: ElementType | None = next(
            (item[0] for item in self.special_mapper if item[1] == name), None)

        if mapped is None:
            mapped: tuple | None = next(
            (item[0] for item in DEFAULT_MAPPING if item[1] == name), None)

        if mapped is None:
            print(f"[WARNING] {name} is unsuported")

        return mapped

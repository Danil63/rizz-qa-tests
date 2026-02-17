"""PageFactory: Элемент текста."""
from tests.elements.base_element import BaseElement


class Text(BaseElement):

    @property
    def type_of(self) -> str:
        return "text"

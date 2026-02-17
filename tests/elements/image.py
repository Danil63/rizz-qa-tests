"""PageFactory: Элемент изображения."""
from tests.elements.base_element import BaseElement


class Image(BaseElement):

    @property
    def type_of(self) -> str:
        return "image"

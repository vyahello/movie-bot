from abc import ABC, abstractmethod
from re import search
from functools import lru_cache


class Text(ABC):
    """Abstraction of a text."""

    @abstractmethod
    def match(self) -> bool:
        pass

    @abstractmethod
    def get(self) -> str:
        pass


class InputText(Text):
    """Parse input text from a message."""

    def __init__(self, text: str, pattern: str = r'\/[\w\s]+') -> None:
        self._pattern = pattern
        self._text = text

    @lru_cache(maxsize=None)
    def match(self) -> bool:
        return search(self._pattern, self._text)

    def get(self) -> str:
        return self.match().group()

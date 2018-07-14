from abc import ABC, abstractmethod
from typing import Dict, Any, Callable
from src.bot import BOT_API_TOKEN
from src.movie.movie import MovieSummary
from src.movie.record import Record
from src.server import requests
from src.web_api.requests import SafeBotRequest, Request
from src.web_api.responses import Response
from src.web_api.urls import HttpsUrlOf


class Answer(ABC):
    """Abstraction for a answer."""

    @abstractmethod
    def chat_id(self) -> int:
        pass

    @abstractmethod
    def message(self) -> str:
        pass


class Message(ABC):
    """Abstraction for a message."""

    @abstractmethod
    def send(self) -> Dict[Any, Any]:
        pass


class BotAnswer(Answer):
    """An answer from a bot."""

    def __init__(self, request: requests.Request) -> None:

        def _req() -> Dict[Any, Any]:
            return request.dct().get('message')

        self._req: Callable[..., Dict[Any, Any]] = _req

    def chat_id(self) -> int:
        return self._req().get('chat').get('id')

    def message(self) -> str:
        return self._req().get('text')


class BotMessage(Message):
    """A message of a bot."""

    def __init__(self, chat_id: int, movie: str) -> None:
        self._chat_id: int = chat_id
        self._movie_summary: Record = MovieSummary(movie)
        self._request: Request = SafeBotRequest(HttpsUrlOf('api.telegram.org/bot', BOT_API_TOKEN, '/sendMessage'))

    def send(self) -> Response:
        return self._request.post({'chat_id': self._chat_id, 'text': self._movie_summary.value()})

from abc import ABC, abstractmethod
from typing import Dict, Any
from src.movie import MOVIE_API_KEY
from src.web_api.requests import Request, SafeBotRequest
from src.web_api.urls import HttpsUrlOf


class Record(ABC):
    """Abstraction of movie data records."""

    @abstractmethod
    def values(self) -> Dict[str, Any]:
        pass


class MovieRecord(Record):
    """Get movie data records."""

    def __init__(self, movie: str) -> None:
        self._request: Request = SafeBotRequest(
            HttpsUrlOf('api.themoviedb.org/3/search/movie?api_key=', MOVIE_API_KEY, '&query=', movie))

    def values(self) -> Dict[str, Any]:
        return self._request.get().json().get('results')[0]

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, TypeVar, Iterator
from src.movie import MOVIE_API_KEY
from src.web_api.requests import Request, SafeBotRequest
from src.web_api.urls import HttpsUrlOf


TypeValue: type = TypeVar('TypeValue', str, int, Dict[str, Any], Iterator[Dict[Any, Any]])


class Record(ABC):
    """Abstraction of movie data records."""

    @abstractmethod
    def value(self) -> TypeValue:
        pass


class MovieId(Record):
    """Get movie id data record."""

    def __init__(self, movie: str) -> None:
        self._request: Request = SafeBotRequest(
            HttpsUrlOf('api.themoviedb.org/3/search/movie?api_key=', MOVIE_API_KEY, '&query=', movie))

    def value(self) -> int:
        return self._request.get().json().get('results')[0].get('id')


class MovieCasts(Record):
    """Get movie casts record."""

    def __init__(self, movie: str) -> None:
        self._request: Callable[..., Request] = lambda: SafeBotRequest(
            HttpsUrlOf('api.themoviedb.org/3/movie/',
                       MovieId(movie).value(), '/credits?api_key=',
                       MOVIE_API_KEY))

    def value(self) -> Iterator[Dict[Any, Any]]:
        for name in self._request().get().json().get('cast'):
            yield name


class MovieRecord(Record):
    """Get movie data records."""

    def __init__(self, movie: str) -> None:
        self._request: Callable[..., Request] = lambda: SafeBotRequest(
            HttpsUrlOf('api.themoviedb.org/3/movie/',
                       MovieId(movie).value(),
                       '?api_key=', MOVIE_API_KEY))

    def value(self) -> Dict[str, Any]:
        return self._request().get().json()

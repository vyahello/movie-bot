from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Dict, Any, Callable
from src.movie.record import Record, MovieRecord, MovieCasts

_star: str = '\u2606'


class Movie(ABC):
    """Abstraction of movie."""

    @abstractmethod
    def title(self) -> str:
        pass

    @abstractmethod
    def rating(self) -> str:
        pass

    @abstractmethod
    def overview(self) -> str:
        pass

    @abstractmethod
    def release_data(self) -> str:
        pass

    @abstractmethod
    def votes(self) -> int:
        pass

    @abstractmethod
    def budget(self) -> int:
        pass

    @abstractmethod
    def revenue(self) -> int:
        pass

    @abstractmethod
    def genres(self) -> str:
        pass

    @abstractmethod
    def casts(self) -> str:
        pass


class MovieDB(Movie):
    """Represent moviedb data values."""

    def __init__(self, movie: str) -> None:

        @lru_cache(maxsize=None)
        def _records() -> Dict[str, Any]:
            return MovieRecord(movie).value()

        self._records: Callable[..., Dict[str, Any]] = _records
        self._casts: Record = MovieCasts(movie)

    def title(self) -> Dict[str, Any]:
        return self._records().get('title')

    def rating(self):
        return self._records().get('vote_average')

    def overview(self) -> str:
        return self._records().get('overview')

    def release_data(self) -> str:
        return self._records().get('release_date')

    def votes(self) -> int:
        return self._records().get('vote_count')

    def budget(self) -> int:
        return self._records().get('budget')

    def revenue(self) -> int:
        return self._records().get('revenue')

    def genres(self) -> str:
        return ', '.join(genre['name'] for genre in self._records().get('genres'))

    def casts(self) -> str:
        cast = self._casts.value()
        return ', '.join(next(cast)['name'] for _ in range(5))


class MovieSummary(Record):
    """Get summary of a movie."""

    def __init__(self, movie: str) -> None:
        self._movie = MovieDB(movie)

    def value(self) -> str:
        return "{star} Title - {title}\n" \
               "{star} Overview - {overview}\n" \
               "{star} Rating - {rating}\n" \
               "{star} Genres - {genres}\n" \
               "{star} Release Date - {date}\n" \
               "{star} Votes - {votes}\n" \
               "{star} Budget - {bugdet}$\n" \
               "{star} Revenue - {revenue}$\n" \
               "{star} Casts - {casts}\n".format(star=_star,
                                                 title=self._movie.title(),
                                                 rating=self._movie.rating(),
                                                 overview=self._movie.overview(),
                                                 date=self._movie.release_data(),
                                                 votes=self._movie.votes(),
                                                 bugdet=self._movie.budget(),
                                                 revenue=self._movie.revenue(),
                                                 genres=self._movie.genres(),
                                                 casts=self._movie.casts())

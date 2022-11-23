from typing import Any, TypeVar

from pydantic import BaseModel, PositiveInt


MODEL_TYEP = TypeVar("MODEL_TYEP")

__all__ = ["PagingParams", "PagingResult", "Msg"]


class Msg(BaseModel):
    msg: str


class PagingParams(BaseModel):
    page: PositiveInt
    per_page: PositiveInt

    class Config:
        allow_population_by_field_name = True

    def populate_result(self, total: int, items: list[Any], **kwargs: Any) -> "PagingResult":
        return PagingResult(page=self.page, per_page=self.per_page, total=total, items=items, **kwargs)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page


class PagingResult(PagingParams):
    total: int
    items: list[Any]

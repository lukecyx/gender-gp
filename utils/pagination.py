from fastapi import Query
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Generic, TypeVar


@dataclass
class PaginationParams:
    page: int = Query(default=1, ge=1)
    page_size: int = Query(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    data: list[T]
    page: int
    page_size: int
    total: int
    total_pages: int

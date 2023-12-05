from typing import Optional, Union, Any

from pydantic import BaseModel, Field
from pytz import common_timezones

from .utils.enums import Order, Operator


class Timeframe(BaseModel):
    gte: Optional[int] = Field(None, alias="from", gte=0)
    lte: Optional[int] = Field(None, alias="to", gte=0)
    field: Optional[str] = Field(None)
    formatDate: Optional[str] = Field(None)


class SearchSchemas(BaseModel):
    field: Optional[str] = Field(None)
    value: Optional[Any] = Field("", examples=[0, ""])
    opt: Optional[Operator | None] = Field(None, examples=Operator.list())


class OrderSchemas(BaseModel):
    order: Optional[Order] = Field(Order.descending, examples=Order.list())
    orderBy: Optional[str] = Field(None)


class TimeframeSchemas(BaseModel):
    timeframe: Optional[Timeframe] = Field(None)
    timezone: Optional[str] = Field("Asia/Jakarta", examples=common_timezones)


class PaginationSchemas(BaseModel):
    page: Optional[int] = Field(None, gte=1)
    size: Optional[int] = Field(None, gte=1)


class OrderedPaginationSchemas(PaginationSchemas, OrderSchemas):
    ...


class OrderedSearchSchemas(SearchSchemas, OrderSchemas):
    ...


class MultiFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas):
    filters: Optional[list[SearchSchemas] | None] = Field(None)


class BaseFilterSchemas(
    PaginationSchemas, TimeframeSchemas, OrderSchemas, SearchSchemas
):
    ...

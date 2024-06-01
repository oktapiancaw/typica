from typing import TypeVar, Optional, Union, List, Dict

from pydantic import BaseModel, Field
from pytz import common_timezones

from .utils import Order, Operator, FilterOption

SearchValueType = TypeVar(
    "SearchValueType", str, int, float, bool, List[str], List[int], None
)


class Timeframe(BaseModel):
    gte: Optional[Union[str, int]] = Field(None, alias="from")
    lte: Optional[Union[str, int]] = Field(None, alias="to")
    field: Optional[str] = Field(None)
    formatDate: Optional[str] = Field(None)


class SearchSchemas(BaseModel):
    field: Optional[str] = Field(None)
    value: Optional[SearchValueType] = Field(None, examples=[0, ""])
    opt: Optional[Union[Operator, None]] = Field(None, examples=Operator.list())


class OrderSchemas(BaseModel):
    order: Optional[Order] = Field(Order.descending, examples=Order.list())
    orderBy: Optional[str] = Field(None)


class TimeframeSchemas(BaseModel):
    timeframe: Optional[Timeframe] = Field(None)
    timezone: Optional[str] = Field("Asia/Jakarta", examples=common_timezones)


class PaginationSchemas(BaseModel):
    page: Optional[int] = Field(1, gte=1)
    size: Optional[int] = Field(10, gte=1)


class OrderedPaginationSchemas(PaginationSchemas, OrderSchemas): ...


class OrderedSearchSchemas(SearchSchemas, OrderSchemas): ...


class MultiFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas):
    filters: Optional[List[SearchSchemas]] = Field(None)


class DynamicFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas):
    filters: Optional[Dict[FilterOption, List[SearchSchemas]]] = Field(None)


class BaseFilterSchemas(
    PaginationSchemas, TimeframeSchemas, OrderSchemas, SearchSchemas
): ...

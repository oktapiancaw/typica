from typing import Optional
from pydantic import BaseModel, Field

from .utils.enums import Order, Operator


class Timeframe(BaseModel):
    gte: Optional[int] = Field(None, alias='from', gte=0)
    lte: Optional[int] = Field(None, alias='to', gte=0)
    field: Optional[str] = Field(None)


class SearchSchemas(BaseModel):
    field: str = Field(None)
    value: int | str = Field('', examples=[0, ''])
    opt: Optional[Operator] = Field(None, examples=Operator.list())


class OrderSchemas(BaseModel):
    order: Optional[Order] = Field(Order.descending, examples=Order.list())
    orderBy: Optional[str] = Field(None)
    
    
class TimeframeSchemas(BaseModel):
    timeframe: Optional[Timeframe] = Field(None)


class PaginationSchemas(BaseModel):
    page: Optional[int] = Field(None, gte=1)
    size: Optional[int] = Field(None, gte=1)
    

class OrderedPaginationSchemas(PaginationSchemas, OrderSchemas):
    ...
    
    
class OrderedSearchSchemas(SearchSchemas, OrderSchemas):
    ...

    
class MultiFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas):
    filters: Optional[list[SearchSchemas]] = Field(None)


class BaseFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas, SearchSchemas):
    ...
    
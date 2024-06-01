from typing import TypeVar, Optional, Union, Any

from pydantic import BaseModel, Field
from pytz import common_timezones

from .utils import Order, Operator, FilterOption
from .utils.query import ChainQuery, _QueryType

SearchValueType = TypeVar(
    "SearchValueType", str, int, float, bool, list[str], list[int], None
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
    filters: Optional[list[SearchSchemas]] = Field(None)


class DynamicFilterSchemas(PaginationSchemas, TimeframeSchemas, OrderSchemas):
    filters: Optional[dict[FilterOption, list[SearchSchemas]]] = Field(None)


class BaseFilterSchemas(
    PaginationSchemas, TimeframeSchemas, OrderSchemas, SearchSchemas
): ...


class MongoQueryBuilder(ChainQuery[_QueryType]):
    def __init__(self) -> None:
        super().__init__()

    def extract_query_must(
        self, filters: list[SearchSchemas]
    ) -> "MongoQueryBuilder[_QueryType]":
        for filter_query in filters:
            if filter_query.opt == Operator.equal:
                self.must({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.unequal:
                self.must({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.include:
                self.must({filter_query.field: {"$in": filter_query.value}})
            elif filter_query.opt == Operator.exclude:
                self.must({filter_query.field: {"$nin": filter_query.value}})
            elif filter_query.opt == Operator.gt:
                self.must({filter_query.field: {"$gt": filter_query.value}})
            elif filter_query.opt == Operator.gte:
                self.must({filter_query.field: {"$gte": filter_query.value}})
            elif filter_query.opt == Operator.lt:
                self.must({filter_query.field: {"$lt": filter_query.value}})
            elif filter_query.opt == Operator.lte:
                self.must({filter_query.field: {"$lte": filter_query.value}})
            elif filter_query.opt == Operator.exist:
                self.must({filter_query.field: {"$exist": 1}})
            elif filter_query.opt == Operator.not_exist:
                self.must({filter_query.field: {"$exist": 0}})
            elif filter_query.opt == Operator.regex:
                self.must(
                    {
                        filter_query.field: {
                            "$regex": filter_query.value,
                            "$options": "i",
                        }
                    }
                )
            else:
                self.must({filter_query.field: filter_query.value})
        return self

    def extract_query_mustnt(
        self, filters: list[SearchSchemas]
    ) -> "MongoQueryBuilder[_QueryType]":
        for filter_query in filters:
            if filter_query.opt == Operator.equal:
                self.mustnt({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.unequal:
                self.mustnt({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.include:
                self.mustnt({filter_query.field: {"$in": filter_query.value}})
            elif filter_query.opt == Operator.exclude:
                self.mustnt({filter_query.field: {"$nin": filter_query.value}})
            elif filter_query.opt == Operator.gt:
                self.mustnt({filter_query.field: {"$gt": filter_query.value}})
            elif filter_query.opt == Operator.gte:
                self.mustnt({filter_query.field: {"$gte": filter_query.value}})
            elif filter_query.opt == Operator.lt:
                self.mustnt({filter_query.field: {"$lt": filter_query.value}})
            elif filter_query.opt == Operator.lte:
                self.mustnt({filter_query.field: {"$lte": filter_query.value}})
            elif filter_query.opt == Operator.exist:
                self.mustnt({filter_query.field: {"$exist": 1}})
            elif filter_query.opt == Operator.not_exist:
                self.mustnt({filter_query.field: {"$exist": 0}})
            elif filter_query.opt == Operator.regex:
                self.mustnt(
                    {
                        filter_query.field: {
                            "$regex": filter_query.value,
                            "$options": "i",
                        }
                    }
                )
            else:
                self.mustnt({filter_query.field: filter_query.value})
        return self

    def extract_query_should(
        self, filters: list[SearchSchemas]
    ) -> "MongoQueryBuilder[_QueryType]":
        for filter_query in filters:
            if filter_query.opt == Operator.equal:
                self.should({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.unequal:
                self.should({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.include:
                self.should({filter_query.field: {"$in": filter_query.value}})
            elif filter_query.opt == Operator.exclude:
                self.should({filter_query.field: {"$nin": filter_query.value}})
            elif filter_query.opt == Operator.gt:
                self.should({filter_query.field: {"$gt": filter_query.value}})
            elif filter_query.opt == Operator.gte:
                self.should({filter_query.field: {"$gte": filter_query.value}})
            elif filter_query.opt == Operator.lt:
                self.should({filter_query.field: {"$lt": filter_query.value}})
            elif filter_query.opt == Operator.lte:
                self.should({filter_query.field: {"$lte": filter_query.value}})
            elif filter_query.opt == Operator.exist:
                self.should({filter_query.field: {"$exist": 1}})
            elif filter_query.opt == Operator.not_exist:
                self.should({filter_query.field: {"$exist": 0}})
            elif filter_query.opt == Operator.regex:
                self.should(
                    {
                        filter_query.field: {
                            "$regex": filter_query.value,
                            "$options": "i",
                        }
                    }
                )
            else:
                self.should({filter_query.field: filter_query.value})
        return self

    def extract_query_shouldnt(
        self, filters: list[SearchSchemas]
    ) -> "MongoQueryBuilder[_QueryType]":
        for filter_query in filters:
            if filter_query.opt == Operator.equal:
                self.shouldnt({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.unequal:
                self.shouldnt({filter_query.field: filter_query.value})
            elif filter_query.opt == Operator.include:
                self.shouldnt({filter_query.field: {"$in": filter_query.value}})
            elif filter_query.opt == Operator.exclude:
                self.shouldnt({filter_query.field: {"$nin": filter_query.value}})
            elif filter_query.opt == Operator.gt:
                self.shouldnt({filter_query.field: {"$gt": filter_query.value}})
            elif filter_query.opt == Operator.gte:
                self.shouldnt({filter_query.field: {"$gte": filter_query.value}})
            elif filter_query.opt == Operator.lt:
                self.shouldnt({filter_query.field: {"$lt": filter_query.value}})
            elif filter_query.opt == Operator.lte:
                self.shouldnt({filter_query.field: {"$lte": filter_query.value}})
            elif filter_query.opt == Operator.exist:
                self.shouldnt({filter_query.field: {"$exist": 1}})
            elif filter_query.opt == Operator.not_exist:
                self.shouldnt({filter_query.field: {"$exist": 0}})
            elif filter_query.opt == Operator.regex:
                self.shouldnt(
                    {
                        filter_query.field: {
                            "$regex": filter_query.value,
                            "$options": "i",
                        }
                    }
                )
            else:
                self.shouldnt({filter_query.field: filter_query.value})
        return self

    def extract_timeframe(
        self, timeframe: Timeframe
    ) -> "MongoQueryBuilder[_QueryType]":
        if timeframe.gte:
            self.must({timeframe.field: {"$gte": timeframe.gte}})
        if timeframe.lte:
            self.must({timeframe.field: {"$lte": timeframe.lte}})
        return self

    @property
    def query_mongo(self) -> dict[str, Any]:
        query_raw = {}
        if self.query.andOpt:
            query_raw["$and"] = self.query.andOpt
        if self.query.orOpt:
            query_raw["$not"] = self.query.orOpt
        if self.query.notOpt:
            query_raw["$or"] = self.query.notOpt
        if self.query.norOpt:
            query_raw["$nor"] = self.query.norOpt
        if self.query.other_query:
            query_raw.update(self.query.other_query)
        return query_raw

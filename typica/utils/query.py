from pydantic import BaseModel, ConfigDict, Field
from typing import Generic, TypeVar, Mapping, Optional, Any


class BaseQuery(BaseModel):
    andOpt: Optional[list[Mapping[str, Any]]] = Field([], description="Must query")
    notOpt: Optional[list[Mapping[str, Any]]] = Field([], description="Must'nt query")
    orOpt: Optional[list[Mapping[str, Any]]] = Field([], description="Should query")
    norOpt: Optional[list[Mapping[str, Any]]] = Field([], description="Shouldnt query")

    model_config = ConfigDict(extra="allow")

    @property
    def other_query(self) -> dict[str, Any]:
        return self.model_dump(
            by_alias=True,
            exclude_none=True,
            exclude={"andOpt", "notOpt", "orOpt", "norOpt"},
        )


_QueryType = TypeVar("_QueryType", bound=Mapping[str, Any])


class ChainQuery(Generic[_QueryType]):
    def __init__(self) -> None:
        self.query: BaseQuery = BaseQuery()

    def add(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query = BaseQuery(**self.query.model_dump(), **query)
        return self

    def must(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.andOpt.append(query)
        return self

    def mustnt(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.notOpt.append(query)
        return self

    def should(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.orOpt.append(query)
        return self

    def shouldnt(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.norOpt.append(query)
        return self

    @property
    def query_json(self) -> dict[str, Any]:
        return self.query.model_dump(
            by_alias=True, exclude_none=True, exclude_defaults=True
        )

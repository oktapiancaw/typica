from pydantic import BaseModel, ConfigDict, Field
from typing import Generic, TypeVar, Mapping, Optional, Any


class BaseQuery(BaseModel):
    andOpt: Optional[list[Mapping[str, Any]]] = Field(None, description="Must query")
    orOpt: Optional[list[Mapping[str, Any]]] = Field(None, description="Should query")
    norOpt: Optional[list[Mapping[str, Any]]] = Field(
        None, description="Shouldnt query"
    )

    model_config = ConfigDict(extra="allow")


_QueryType = TypeVar("_QueryType", bound=BaseQuery)


class ChainQuery(Generic[_QueryType]):
    def __init__(self) -> None:
        self.query: _QueryType = BaseQuery()

    def add(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.update(query)
        return self

    def must(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.andOpt.append(query)
        return self

    def should(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.orOpt.append(query)
        return self

    def shouldnt(self, query: _QueryType) -> "ChainQuery[_QueryType]":
        self.query.norOpt.append(query)
        return self

    @property
    def query_json(self) -> dict[str, Any]:
        return self.query.model_dump(by_alias=True, exclude_none=True)

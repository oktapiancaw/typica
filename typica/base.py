from uuid import uuid4
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, UUID4
from pytz import common_timezones

from .utils.enums import DataStatus


class IdMeta(BaseModel):
    """
    Only id
    """

    id: UUID4 = Field(default_factory=uuid4)


class IdMongoMeta(BaseModel):
    """
    _id support for mongo
    """

    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")


# * Basic metadata
class MetaCreate(BaseModel):
    """
    Default create metadata
    """

    createdAt: Optional[int] = Field(
        default_factory=lambda: int(datetime.now().timestamp() * 1000), ge=0
    )
    createdBy: Optional[str] = Field("")


class MetaUpdate(BaseModel):
    """
    Default update metadata
    """

    updatedAt: Optional[int] = Field(None)
    updatedBy: Optional[str] = Field(None)


class MetaDelete(BaseModel):
    """
    Default delete metadata
    """

    updatedAt: Optional[int] = Field(None)
    deletedBy: Optional[str] = Field(None)


class MetaAdditional(BaseModel):
    """
    Default additionals metadata
    """

    timezone: Optional[str] = Field("Asia/Jakarta", examples=common_timezones)
    status: Optional[DataStatus] = Field(DataStatus.active, examples=DataStatus.list())

    @property
    def is_active(self):
        return self.status == DataStatus.active

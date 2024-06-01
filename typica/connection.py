import re

from abc import ABC, abstractmethod
from typing import Optional, Union, TypeVar, List

from deprecated import deprecated
from pydantic import BaseModel, Field, model_validator

from .utils import ConnectionTypes

connectionType = TypeVar("connectionType", ConnectionTypes, str, None)


class HostMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[int] = Field(8000, description="Connection port")


@deprecated(
    version="0.1.11", reason="use DatabaseConnectionMeta or QueueConnectionMeta instead"
)
class ConnectionMeta(HostMeta):
    """
    Base connection metadata model
    """

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    database: Optional[Union[str, int]] = Field(None, description="Database name")
    clustersUri: Optional[List[HostMeta]] = Field(None)

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        meta = ""
        if self.clustersUri:
            temp = []
            for cluster in self.clustersUri:
                temp.append(f"{cluster.host}:{cluster.port}")
            meta = ",".join(temp)
        else:
            meta = f"{self.host}:{self.port}"
        if self.username:
            return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db else ''}"
        return f"{base}://{meta}/{self.database if with_db else ''}"


class DatabaseConnectionMeta(HostMeta):

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    database: Optional[Union[str, int]] = Field(None, description="Database name")
    uri: Optional[str] = Field("", description="")

    def uri_string(self, base: str = "http", with_db: bool = True) -> str:
        meta = f"{self.host}:{self.port}"
        if self.username:
            return f"{base}://{self.username}:{self.password}@{meta}/{self.database if with_db else ''}"
        return f"{base}://{meta}/{self.database if with_db else ''}"

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                self.username, self.password, self.host, self.port = re.split(
                    r"\@|\:", metadata
                )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            self.port = int(self.port)
        return self


class QueueConnectionMeta(HostMeta):

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    clustersUri: Optional[List[HostMeta]] = Field(None)
    uri: Optional[str] = Field("", description="")

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                if "," in metadata:
                    metadata, raw_clusters = re.split(r"\@", metadata)
                    self.username, self.password = re.split(r"\:", metadata)
                    clustersUri = []
                    for cluster in raw_clusters.split(","):
                        hostData = re.split(r"\:", cluster)
                        clustersUri.append(HostMeta(host=hostData[0], port=hostData[1]))
                    self.clustersUri = clustersUri
                else:
                    self.username, self.password, self.host, self.port = re.split(
                        r"\@|\:", metadata
                    )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            self.port = int(self.port)
        return self


database_meta_type = TypeVar("database_meta_type", DatabaseConnectionMeta, HostMeta)
queue_meta_type = TypeVar("queue_meta_type", DatabaseConnectionMeta, HostMeta)


@deprecated(
    version="0.1.11", reason="use DatabaseConnectionMeta or QueueConnectionMeta instead"
)
class ConnectionUriMeta(ConnectionMeta):
    """Connection with URI and connection types metadata model

    Args:
        ConnectionMeta (BaseModel): Base connection metadata model

    Returns:
        ConnectionMeta: parsed connection metadata from URI
    """

    uri: Optional[str] = Field("", description="")
    type_connection: Optional[connectionType] = Field(
        None, examples=ConnectionTypes.list()
    )

    @model_validator(mode="after")
    def extract_uri(self):
        if self.uri:
            uri = re.sub(r"\w+:(//|/)", "", self.uri)
            metadata, others = (
                re.split(r"\/\?|\/", uri) if re.search(r"\/\?|\/", uri) else [uri, None]
            )
            if others and "&" in others:
                for other in others.split("&"):
                    if "=" in other and re.search(r"authSource", other):
                        self.database = other.split("=")[-1]
                    elif "=" not in other:
                        self.database = other
            if "@" in metadata:
                if "," in metadata:
                    metadata, raw_clusters = re.split(r"\@", metadata)
                    self.username, self.password = re.split(r"\:", metadata)
                    clustersUri = []
                    for cluster in raw_clusters.split(","):
                        hostData = re.split(r"\:", cluster)
                        clustersUri.append(HostMeta(host=hostData[0], port=hostData[1]))
                    self.clustersUri = clustersUri
                else:
                    self.username, self.password, self.host, self.port = re.split(
                        r"\@|\:", metadata
                    )
            else:
                self.host, self.port = re.split(r"\:", metadata)
            self.port = int(self.port)
        return self


connectionPayload = TypeVar("connectionPayload", ConnectionMeta, ConnectionUriMeta)


@deprecated(version="0.1.11", reason="use DatabaseConnector or QueueConnector instead")
class BaseConnection(ABC):
    def __init__(self, metadata: connectionPayload) -> None:
        self._metadata = metadata

    @abstractmethod
    def close(self) -> None:
        pass


class BaseConnector(ABC):
    def __init__(self) -> None:
        pass


class DatabaseConnector(BaseConnector):
    def __init__(self, meta: database_meta_type) -> None:
        self._meta: database_meta_type = meta
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def get_data(self, table: str, query: any, **kwargs):
        pass

    @abstractmethod
    def insert_data(self, table: str, data: any, **kwargs):
        pass

    @abstractmethod
    def update_data(self, table: str, query: any, data: any, **kwargs):
        pass

    @abstractmethod
    def delete_data(self, table: str, query: any, **kwargs):
        pass

    @abstractmethod
    def bulk_insert_data(self, table: str, data: List[any], **kwargs):
        pass

    @abstractmethod
    def scan_data(self, table: str, query: any, **kwargs):
        pass


class QueueConnector(BaseConnector):
    def __init__(self, meta: queue_meta_type) -> None:
        self._meta: queue_meta_type = meta
        pass

    @abstractmethod
    def consumer_connect(self, queue: str, **kwargs):
        pass

    @abstractmethod
    def producer_connect(self, queue: str, **kwargs):
        pass

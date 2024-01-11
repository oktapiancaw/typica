import re
from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

from .utils.enums import ConnectionTypes


class HostMeta(BaseModel):
    host: Optional[str] = Field("localhost", description="Connection host")
    port: Optional[int] = Field(8000, description="Connection port")


class ConnectionMeta(HostMeta):
    """
    Base connection metadata model
    """

    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    database: Optional[Union[str, int]] = Field(None, description="Database name")
    clustersUri: Optional[list[HostMeta] | None] = Field(None)

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


class ConnectionUriMeta(ConnectionMeta):
    """Connection with URI and connection types metadata model

    Args:
        ConnectionMeta (BaseModel): Base connection metadata model

    Returns:
        ConnectionMeta: parsed connection metadata from URI
    """

    uri: Optional[str] = Field("", description="")
    type_connection: Optional[ConnectionTypes | None] = Field(
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


class BaseConnection:
    def __init__(self, metadata: ConnectionMeta | ConnectionUriMeta) -> None:
        self._metadata = metadata

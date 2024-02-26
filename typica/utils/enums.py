from enum import Enum


class EnumV2(Enum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class EnumV3(EnumV2):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, value, description: str = None):
        self._value_ = value
        self._description_ = description

    @property
    def description(self):
        return self._description_


class Order(EnumV3):
    ascending = ("ASC", "sorted ascending")
    descending = ("DESC", "sorted descending")


class Operator(EnumV3):
    equal = ("eq", "value is equals to")
    unequal = ("ne", "value isn't equals to")
    regex = ("re", "regex match")
    gte = ("gte", "value is greater equals to")
    gt = ("gt", "value is greater to")
    lte = ("lte", "value is lower equals to")
    lt = ("lt", "value is lower to")
    include = ("in", "values that must exist")
    exclude = ("nin", "values that don't exist")
    exist = ("exist", "value is exist")
    not_exist = ("exist", "value is exist")


class DataStatus(str, EnumV2):
    """
    Default status of data
    """

    active = "active"
    archive = "archive"
    deleted = "deleted"
    success = "success"
    failed = "failed"
    published = "published"
    unpublished = "unpublished"


class ConnectionTypes(str, EnumV2):
    """
    Connection types supported on ConnectionUriMeta
    """

    clickhouse = "clickhouse"
    elastic = "elasticsearch"
    mongo = "mongo"
    postgre = "postgresql"
    mysql = "mysql"
    redis = "redis"


class ResponseMessage(str, EnumV2):
    """
    Base response service
    """

    ok = "OK"
    failed = "Failed"
    success = "Success"
    update = "Updated"
    delete = "Deleted"
    archive = "Archived"


class ErrorResponseMessage(str, EnumV2):
    """
    Base error response service
    """

    # * base
    alreadyExist = "is already exist"
    isNotExist = "isn't exist"
    isInvalid = "is invalid"
    notFound = "isn't found"
    expired = "is expired"

    # * with sub/ob-ject
    dataAlreadyExist = "Data is already exist"
    dataIsNotExist = "Data isn't exist"
    dataIsInvalid = "Data is invalid"
    dataNotFound = "Data isn't found"
    tokenExpired = "Token is expired"

    # * others
    forbidden = "Forbidden access"
    unAuthz = "Unathorized"
    wentWrong = "Service error, please tell admin"

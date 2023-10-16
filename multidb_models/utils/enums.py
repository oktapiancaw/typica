from enum import Enum


class UpgradedEnum(Enum):
    
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class Order(str, UpgradedEnum):
    ascending = 'ASC'
    descending = 'DESC'


class Operator(str, UpgradedEnum):
    equal = 'equal'
    unequal = 'unequal'
    regex = 'regex'
    gte = 'gte'
    gt = 'gt'
    lte = 'lte'
    lt = 'lt'
    include = 'include'
    exclude = 'exclude'


class DataStatus(str, UpgradedEnum):
    """
    Default status of data
    """

    active = "active"
    archive = "archive"
    deleted = "deleted"
    success = "success"
    failed = "failed"


class ConnectionTypes(str, UpgradedEnum):
    """
    Connection types supported on ConnectionUriMeta
    """

    clickhouse = "clickhouse"
    elastic = "elasticsearch"
    mongo = "mongo"
    postgre = "postgresql"
    mysql = "mysql"
    redis = "redis"


class ResponseMessage(str, UpgradedEnum):
    """
    Base response service
    """

    ok = "OK"
    failed = "Failed"
    success = "Success"
    update = "Updated"
    delete = "Deleted"
    archive = "Archived"


class ErrorResponseMessage(str, UpgradedEnum):
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

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

    def __init__(self, value, description: str | None = None):
        self._value_ = value
        self._description_ = description

    @property
    def description(self):
        return self._description_

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


class FilterOption(EnumV3):
    must = ("must", "List of filter must exact")
    mustnt = ("mustnt", "List of filter mustn't exact")
    should = ("should", "List of filter should exact")
    shouldnt = ("shouldnt", "List of filter shouldn't exact")

class LocationLevel(str, EnumV3):
    CONTINENT = ("continent", "Continent level data")
    COUNTRY = ("country", "Country level data")
    PROVINCE = ("province", "Province level data")
    CITY = ("city", "City level data")
    DISTRICT = ("district", "District level data")
    SUBDISTRICT = ("subdistrict", "Subdistrict level data")


class MedallionTypes(str, EnumV3):
    LAKE = ("lake", 'Lake data')
    BRONZE = ("bronze", 'bronze level Medallion')
    SILVER = ("silver", 'silver level Medallion')
    GOLD = ("gold", 'gold level Medallion')
    OTHER = ("other", 'other than any level Medallion')


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

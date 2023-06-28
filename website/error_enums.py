from enum import Enum


class ErrorEnum(Enum):
    DATE_TOO_FAR_IN_FUTURE = (
        "Unable to give a weather forecast this far into the future!"
    )
    DATE_TOO_FAR_IN_PAST = "Unable to give weather forecast this far into the past!"
    ERROR_FETCHING_IMAGE = "Error occurred while fetching a static image"
    ERROR_FETCHING_MAP = "Error occured whilte fetching google maps data"
    INVALID_CITY = "Not a valid city, please try again!"
    REQUEST_FAILED = "Could not make a successfull request"

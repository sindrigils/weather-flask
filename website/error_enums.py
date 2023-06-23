from enum import Enum


class ErrorEnum(Enum):
    DATE_TOO_FAR_IN_FUTURE = (
        "Unable to give a weather forecast this far into the future!"
    )

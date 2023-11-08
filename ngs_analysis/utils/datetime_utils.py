import re


def get_year(datetime: str) -> str:
    if datetime == "":
        return datetime

    datetime_split = datetime.split("-")
    if len(datetime_split) == 3:
        return datetime_split[-1]
    elif len(datetime_split) == 2:
        return datetime_split[0]
    return datetime_split[0]

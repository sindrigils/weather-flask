from datetime import datetime


def format_date(date: str) -> str:
    date_obj = datetime.strptime(date, "%Y-%m-%d")

    return date_obj.strftime("%d %B %Y")

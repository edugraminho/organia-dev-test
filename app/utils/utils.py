import re
from urllib.parse import urlparse
from datetime import datetime
from .variables import FULL_DATE_FORMAT, DATE_FORMAT


def convert_date_to_timestamp(date: str, format: str = DATE_FORMAT) -> int:
    timestamp = datetime.strptime(date, format).timestamp()
    return int(timestamp)

def convert_full_date_to_timestamp(date: str) -> int:
    timestamp = datetime.strptime(date, FULL_DATE_FORMAT).timestamp()
    return int(timestamp)

def convert_timestamp_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d")
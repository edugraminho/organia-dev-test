from datetime import datetime
from .variables import DATE_FORMAT


def convert_date_to_timestamp(date: str, format: str = DATE_FORMAT) -> int:
    """
    Converts a date string into a timestamp.

    Args:
        date (str): The date string to be converted.
        format (str, optional): The format of the date string. Defaults to DATE_FORMAT.

    Returns:
        int: The timestamp representation of the given date.

    Raises:
        ValueError: If the input date does not match the expected format.
    """
    timestamp = datetime.strptime(date, format).timestamp()
    return int(timestamp)


def convert_timestamp_to_date(timestamp: int) -> str:
    """
    Converts a timestamp into a formatted date string.

    Args:
        timestamp (int): The timestamp to be converted.

    Returns:
        str: The formatted date string in "YYYY/MM/DD" format.
    """
    return datetime.fromtimestamp(timestamp).strftime("%Y/%m/%d")

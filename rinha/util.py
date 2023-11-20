from datetime import datetime


def is_valid_date(date_as_str) -> bool:
    try:
        datetime.strptime(date_as_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_valid_stack(stack) -> bool:
    return all(isinstance(item, str) for item in stack)

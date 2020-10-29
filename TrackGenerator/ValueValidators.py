

def validate_greater_equal_zero(value: float):
    """
    Validates a given number is greater or equal to zero.
    :param value: The number to check.
    """
    if value < 0:
        raise ValueError("Value must be greater or equal to zero!")


def validate_greater_zero(value: float):
    """
    Validates a given number is greater than zero.
    :param value: The number to check.
    """
    if value <= 0:
        raise ValueError("Value must be greater or equal to zero!")

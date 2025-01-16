def map(value, min1, max1, min2, max2):
    """
    Maps a value from one range to another range.

    Args:
        value (float): The value to be mapped.
        min1 (float): The minimum of the first range.
        max1 (float): The maximum of the first range.
        min2 (float): The minimum of the second range.
        max2 (float): The maximum of the second range.

    Returns:
        float: The mapped value.
    """
    return (value - min1) / (max1 - min1) * (max2 - min2) + min2

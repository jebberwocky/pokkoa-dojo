import time


def store_string_with_expiry(string, filename, expiry_seconds):
    """
    Stores a string in a local file with an expiration time.

    Args:
        string (str): The string to be stored.
        filename (str): The name of the file to store the string.
        expiry_seconds (int): The number of seconds until the file expires.
    """
    expiry_time = time.time() + expiry_seconds

    with open(filename, 'w') as file:
        file.write(string + '\n')
        file.write(str(expiry_time))


def read_string_with_expiry(filename):
    """
    Reads a string from a local file, checking if it has expired.

    Args:
        filename (str): The name of the file containing the string.

    Returns:
        str: The stored string if it has not expired, otherwise None.
    """
    try:
        with open(filename, 'r') as file:
            string = file.readline().strip()
            expiry_time = float(file.readline())

        if time.time() < expiry_time:
            return string
        else:
            return None
    except (FileNotFoundError, ValueError):
        return None
import os


def parse_initial_query():
    """
    Gets the INITIAL_QUERY environment variable and parses it into an array of strings.
    Returns a list of trimmed query strings with quotation marks removed.
    """

    query = os.getenv("INITIAL_QUERY", "")
    if not query:
        return []

    # Split by comma, trim whitespace, and remove quotes from each item
    return [item.strip().replace('"', "").replace("'", "") for item in query.split(",")]


def get_env_var(var_name):
    value = os.getenv(var_name)
    return value.replace('"', "") if value else value

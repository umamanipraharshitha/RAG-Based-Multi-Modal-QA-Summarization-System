import os
from dotenv import load_dotenv

def load_env_var(key: str, default: str | None = None) -> str:
    """
    Safely load an environment variable from .env or system.

    Args:
        key (str): The environment variable name.
        default (str | None): Default value if variable is missing.

    Returns:
        str: The value of the environment variable.

    Raises:
        EnvironmentError: If variable is missing and no default is provided.
    """
    load_dotenv()
    val = os.getenv(key, default)
    if val is None:
        raise EnvironmentError(f"Missing required env var: {key}")
    return val

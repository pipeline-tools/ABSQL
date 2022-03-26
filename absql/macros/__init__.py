from .env import env_var
from .db import table_exists, query_db
from datetime import datetime, timedelta


default_macros = {
    "datetime": datetime,
    "env_var": env_var,
    "table_exists": table_exists,
    "timedelta": timedelta,
    "query_db": query_db,
}
default_constructors = {"!" + k: v for k, v in default_macros.items()}

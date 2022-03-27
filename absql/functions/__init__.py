from .env import env_var, env_switch
from .db import table_exists, query_db, get_max_value, get_min_value
from .time import previous_date, previous_hour
from datetime import datetime, timedelta


default_functions = {
    "datetime": datetime,
    "env_switch": env_switch,
    "env_var": env_var,
    "get_max_value": get_max_value,
    "get_min_value": get_min_value,
    "previous_date": previous_date,
    "previous_hour": previous_hour,
    "table_exists": table_exists,
    "timedelta": timedelta,
    "query_db": query_db,
}
default_constructors = {
    "!" + k: v
    for k, v in default_functions.items()
    if k
    in (
        "datetime",
        "env_switch",
        "env_var",
        "previous_date",
        "previous_hour",
        "timedelta",
    )
}

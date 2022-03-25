from .env import env_var
from .db import table_exists
from datetime import datetime, timedelta


# add query macro (accept string or sqlalchemy engine)
# add env_switch macro
default_macros = {
    "env_var": env_var,
    "datetime": datetime,
    "timedelta": timedelta,
    "engine": None,
    "table_exists": table_exists,
}
default_constructors = {"!" + k: v for k, v in default_macros.items()}

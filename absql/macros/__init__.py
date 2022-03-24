from .env import env_var
from datetime import datetime, timedelta


default_macros = {"env_var": env_var, "datetime": datetime, "timedelta": timedelta}
default_constructors = {"!" + k: v for k, v in default_macros.items()}

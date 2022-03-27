import os


def env_var(var, default=None):
    return os.environ.get(var, default)

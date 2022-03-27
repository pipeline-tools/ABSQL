import os


def env_var(var, default=None):
    return os.environ.get(var, default)


def env_switch(default=None, **kwargs):
    value_unspecified = "value_unspecified"
    if default is None:
        default = value_unspecified
    # What is the environment variable that
    # tells us what environment we are in?
    env_env_var = env_var("AB__ENV", "ENV")
    # What environment are we in?
    env = env_var(env_env_var, value_unspecified)
    # What is the value that corresponds to the environment?
    value = kwargs.get(env, default)
    return value

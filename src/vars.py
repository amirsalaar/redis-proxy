import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

env_vars_store = {
    **os.environ,
    **dotenv_values(".env"),
    **dotenv_values(".env.local"),
}

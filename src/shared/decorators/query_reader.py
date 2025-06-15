import os
from functools import wraps


def sql_query_reader(base_dir, relative_path):

    sql_folder = os.path.join(base_dir, "sql")
    query_file = os.path.join(sql_folder, relative_path)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with open(query_file, "r") as file:
                    wrapper.query = file.read()
            except FileNotFoundError:
                raise FileNotFoundError(f"The file {query_file} was not found")
            return func(*args, **kwargs)

        return wrapper

    return decorator

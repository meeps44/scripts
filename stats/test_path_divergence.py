from lib.definitions.classdefinitions import *
from lib.sqlite_load import *
import time
import pytest
import pandas as pd
from os.path import expanduser
import matplotlib.pyplot as plt

home = expanduser("~")
# db_name = "sample-200.csv"
# db_location = home + "/git/scripts/stats/tests/sample-data/" + db_name
# data: pd.DataFrame = pd.read_csv(db_location)

db_path = "/home/erlend/db-storage/large-data/" + Databases.ams
data: pd.DataFrame = load_single(db_path)


def get_unique_routers_where_a_path_change_occurred(df: pd.DataFrame) -> list:
    """
    Return a list of all routers (IP-addresses) where a change in path
    was detected.
    """
    pass

from enum import Enum
from dataclasses import dataclass


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0


class VantagePoint(Enum):
    ams3 = 1
    blr1 = 2
    fra1 = 3
    lon1 = 4
    nyc1 = 5
    sfo3 = 6
    sgp1 = 7
    tor1 = 8

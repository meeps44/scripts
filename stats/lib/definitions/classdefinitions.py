from enum import Enum, IntEnum
from dataclasses import dataclass, asdict


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0
    num_asns_traversed: int = 0


@dataclass
class SourceIPAddresses:
    ams3: str = ""
    blr1: str = ""
    fra1: str = ""
    lon1: str = ""
    nyc1: str = ""
    sfo3: str = ""
    sgp1: str = ""
    tor1: str = ""

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


class VantagePoint(Enum):
    ams3 = 1
    blr1 = 2
    fra1 = 3
    lon1 = 4
    nyc1 = 5
    sfo3 = 6
    sgp1 = 7
    tor1 = 8


class FlowLabels(IntEnum):
    FL_0 = 0
    FL_255 = 255
    FL_65280 = 65280
    FL_983040 = 983040
    FL_1048575 = 1048575

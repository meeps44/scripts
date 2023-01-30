from enum import Enum
from dataclasses import dataclass


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_loops: int = 0
    num_fl_changes: int = 0

@dataclass
class SourceIPAddresses:
    ams3:str = ""
    blr1:str = ""
    fra1:str = ""
    lon1:str = ""
    nyc1:str = ""
    sfo3:str = ""
    sgp1:str = ""
    tor1:str = ""

    def to_dict():
        ip_addresses = {
            "ams3" : "",
            "blr1" : "",
            "fra1" : "",
            "lon1" : "",
            "nyc1" : "",
            "sfo3" : "",
            "sgp1" : "",
            "tor1" : "",
        }
        return ip_addresses

class VantagePoint(Enum):
    ams3 = 1
    blr1 = 2
    fra1 = 3
    lon1 = 4
    nyc1 = 5
    sfo3 = 6
    sgp1 = 7
    tor1 = 8

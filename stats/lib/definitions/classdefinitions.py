from enum import Enum, IntEnum
from dataclasses import dataclass, asdict


@dataclass
class TracerouteStatistics:
    num_rows_total: int = 0
    num_cycles: int = 0
    num_cycle_rows: int = 0
    num_loops: int = 0
    num_loop_rows: int = 0
    num_fl_changes: int = 0
    num_fl_change_rows: int = 0
    num_unique_asns_in_dataset: int = 0
    num_invalid_rows: int = 0
    n_traceroutes_to_the_same_destination_with_the_same_flow_label: int = 2
    num_vantage_points: int = 8


@dataclass
class DefaultGateways:
    ams3: str = "2a03:b0c0:2:d0::1"
    blr1: str = "2400:6180:100:d0::1"
    fra1: str = "2a03:b0c0:3:d0::1"
    lon1: str = "2a03:b0c0:1:d0::1"
    nyc1: str = "2604:a880:400:d0::1"
    sfo3: str = "2604:a880:4:1d0::1"
    sgp1: str = "2400:6180:0:d0::1"
    tor1: str = "2604:a880:cad:d0::1"


@dataclass
class DefaultGatewayASN:
    ams3: str = "14061"
    blr1: str = "14061"
    fra1: str = "14061"
    lon1: str = "14061"
    nyc1: str = "14061"
    sfo3: str = "14061"
    sgp1: str = "14061"
    tor1: str = "14061"


@dataclass
class SourceIPAddresses:
    ams3: str = "2a03:b0c0:2:d0::4b5:6001/64"
    blr1: str = "2400:6180:100:d0::9e8:9001/64"
    fra1: str = "a03:b0c0:3:d0::128f:c001/64"
    lon1: str = "2a03:b0c0:1:d0::127f:9001/64"
    nyc1: str = "2604:a880:400:d0::1ce4:b001/64"
    sfo3: str = "2604:a880:4:1d0::6bb:e000/64"
    sgp1: str = "2400:6180:0:d0::fb5:d001/64"
    tor1: str = "2604:a880:cad:d0::f06:4001/64"

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class OldSourceIPAddresses:
    ams3: str = "2a03:b0c0:2:d0::dd6:f001"
    blr1: str = "2400:6180:100:d0::896:a001"
    fra1: str = "2a03:b0c0:3:d0::1771:d001"
    lon1: str = "2a03:b0c0:1:d0::12c1:a001"
    nyc1: str = "2604:a880:400:d0::2573:a001"
    sfo3: str = "2604:a880:4:1d0::76a:b000"
    sgp1: str = "2400:6180:0:d0::1662:6001"
    tor1: str = "2604:a880:cad:d0::e4c:a001"

    def to_dict(self):
        return {k: str(v) for k, v in asdict(self).items()}


@dataclass
class Databases:
    ams: str = "db-ubuntu-ams3-0-2023-04-12T19_33_26Z.db"
    blr: str = "db-ubuntu-blr1-0-2023-04-12T19_33_26Z.db"
    fra: str = "db-ubuntu-fra1-0-2023-04-12T19_33_26Z.db"
    lon: str = "db-ubuntu-lon1-0-2023-04-12T19_33_26Z.db"
    nyc: str = "db-ubuntu-nyc1-0-2023-04-12T19_33_26Z.db"
    sfo: str = "db-ubuntu-sfo3-0-2023-04-12T19_33_26Z.db"
    sgp: str = "db-ubuntu-sgp1-0-2023-04-12T19_33_26Z.db"
    tor: str = "db-ubuntu-tor1-0-2023-04-12T19_33_26Z.db"


@dataclass
class OldDatabases:
    ams: str = "db-ubuntu-ams3-0-2023-01-19T23_00_25Z.db"
    blr: str = "db-ubuntu-blr1-0-2023-01-19T23_00_25Z.db"
    fra: str = "db-ubuntu-fra1-0-2023-01-19T23_00_25Z.db"
    lon: str = "db-ubuntu-lon1-0-2023-01-19T23_00_25Z.db"
    nyc: str = "db-ubuntu-nyc1-0-2023-01-19T23_00_25Z.db"
    sfo: str = "db-ubuntu-sfo3-0-2023-01-19T23_00_25Z.db"
    sgp: str = "db-ubuntu-sgp1-0-2023-01-19T23_00_25Z.db"
    tor: str = "db-ubuntu-tor1-0-2023-01-19T23_00_25Z.db"


@dataclass
class VantagePoint:
    ams: str = "ams3"
    blr: str = "blr1"
    fra: str = "fra1"
    lon: str = "lon1"
    nyc: str = "nyc1"
    sfo: str = "sfo3"
    sgp: str = "sgp1"
    tor: str = "tor1"


@dataclass
class VPFullNames:
    ams: str = "Amsterdam, the Netherlands"
    blr: str = "Bangalore, India"
    fra: str = "Frankfurt, Germany"
    lon: str = "London, United Kingdom"
    nyc: str = "New York, United States"
    sfo: str = "San Francisco, United States"
    sgp: str = "Singapore"
    tor: str = "Toronto, Canada"


# class FlowLabels(IntEnum):
class FlowLabels():
    FL_0 = 0
    FL_255 = 255
    FL_65280 = 65280
    FL_983040 = 983040
    FL_1048575 = 1048575

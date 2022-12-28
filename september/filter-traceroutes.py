import pandas as pd
import numpy as np

# Main filtering functions:


def filter_loops(df) -> pd.DataFrame:
    """Remove from a dataframe all traceroute loops."""
    filtered_count: int = 0
    # Print the number of elements filtered
    print(filtered_count)
    return new_df


def filter_cycles(df) -> pd.DataFrame:
    """Filter from a dataframe all traceroute cycles."""
    filtered_count: int = 0
    # Print the number of elements filtered
    print(filtered_count)
    return new_df


def filter_changed_flowlabel(df) -> pd.DataFrame:
    """Remove from a dataframe all traceroute pairs containing a changed flow label."""
    filtered_count: int = 0
    # Print the number of elements filtered
    print(filtered_count)
    return new_df


def filter_changed_path(df) -> pd.DataFrame:
    """Remove from a dataframe all traceroute pairs containing a changed path."""
    filtered_count: int = 0
    # Print the number of elements filtered
    print(filtered_count)
    return new_df

# Helper functions:


def compare_column_values(df: pd.DataFrame, row1: int, row2: int, column_name: str) -> bool:
    """Compare two column values at the specified rows."""
    return df.loc[row1, column_name] == df.loc[row2, column_name]


def compare_ip_addresses(df: pd.DataFrame, row: int, column1: int, column2: int) -> bool:
    """Compare two IP-addresses at the specified column indexes."""
    return df.loc[row, column1] == df.loc[row, column2]


def main():
    pass


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Analyze Canadian National Fire Database ignition point data and generate plots.

This script prints summary statistics and optionally creates several simple
visualizations.  It defaults to using ``NFDB_point_20240613.txt`` in the current
directory but the data file path can be overridden with a command line option.
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DATA_FILE = "NFDB_point_20240613.txt"


def parse_args():
    """Return parsed command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--file",
        default=DATA_FILE,
        help="Path to NFDB ignition point text file",
    )
    parser.add_argument(
        "--sample-size",
        type=int,
        default=10000,
        help="Number of locations to plot in the scatter plot",
    )
    parser.add_argument(
        "--cause-sample-size",
        type=int,
        default=5000,
        help="Locations per cause for cause-based scatter plots",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating image files",
    )
    return parser.parse_args()


def load_data(path: Path) -> pd.DataFrame:
    """Load relevant columns from the dataset."""
    cols = ["LATITUDE", "LONGITUDE", "YEAR", "SIZE_HA", "CAUSE"]
    return pd.read_csv(path, usecols=cols)


def summary(df: pd.DataFrame) -> None:
    """Print basic summary statistics."""
    total_fires = len(df)
    avg_size = df["SIZE_HA"].mean()
    median_size = df["SIZE_HA"].median()
    print(f"Total fires: {total_fires}")
    print(f"Average size (ha): {avg_size:.2f}")
    print(f"Median size (ha): {median_size:.2f}")
    print("\nCauses:\n" + df["CAUSE"].value_counts().to_string())


def plot_fires_per_year(df: pd.DataFrame) -> None:
    """Save bar chart of fires per year."""
    yearly = df['YEAR'].value_counts().sort_index()
    plt.figure(figsize=(10, 4))
    yearly.plot(kind='bar')
    plt.xlabel('Year')
    plt.ylabel('Number of Fires')
    plt.title('Fires per Year')
    plt.tight_layout()
    plt.savefig('fires_per_year.png')
    plt.close()


def plot_causes(df: pd.DataFrame) -> None:
    """Save bar chart of fire causes."""
    causes = df['CAUSE'].value_counts()
    plt.figure(figsize=(6, 4))
    causes.plot(kind='bar')
    plt.xlabel('Cause')
    plt.ylabel('Count')
    plt.title('Fire Causes')
    plt.tight_layout()
    plt.savefig('fire_causes.png')
    plt.close()


def plot_sample_locations(df: pd.DataFrame, n: int = 10000) -> None:
    """Save scatter plot of a sample of fire locations."""
    sample = df[['LONGITUDE', 'LATITUDE']].sample(min(n, len(df)), random_state=42)
    plt.figure(figsize=(6, 6))
    plt.scatter(sample['LONGITUDE'], sample['LATITUDE'], s=1, alpha=0.3)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Sample Fire Locations')
    plt.tight_layout()
    plt.savefig('fire_locations_sample.png')
    plt.close()


def plot_yearly_by_cause(df: pd.DataFrame) -> None:
    """Save line chart of yearly fire counts for each cause."""
    by_year = df.groupby(["YEAR", "CAUSE"]).size().unstack(fill_value=0)
    plt.figure(figsize=(10, 4))
    by_year.plot()
    plt.xlabel("Year")
    plt.ylabel("Number of Fires")
    plt.title("Fires per Year by Cause")
    plt.tight_layout()
    plt.savefig("fires_by_cause_year.png")
    plt.close()


def plot_locations_by_cause(df: pd.DataFrame, n: int = 5000) -> None:
    """Save scatter plots of fire locations for each cause."""
    for cause, group in df.groupby("CAUSE"):
        sample = group[["LONGITUDE", "LATITUDE"]].sample(
            min(n, len(group)), random_state=42
        )
        plt.figure(figsize=(6, 6))
        plt.scatter(sample["LONGITUDE"], sample["LATITUDE"], s=1, alpha=0.3)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Locations - {cause}")
        plt.tight_layout()
        fname = f"fire_locations_{cause}.png".replace("/", "_")
        plt.savefig(fname)
        plt.close()


def main() -> None:
    args = parse_args()
    data_path = Path(args.file)
    df = load_data(data_path)
    summary(df)
    if not args.no_plots:
        plot_fires_per_year(df)
        plot_causes(df)
        plot_sample_locations(df, n=args.sample_size)
        plot_yearly_by_cause(df)
        plot_locations_by_cause(df, n=args.cause_sample_size)


if __name__ == '__main__':
    main()

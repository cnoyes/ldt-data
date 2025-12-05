#!/usr/bin/env python3
"""
Generate version-controlled metadata from conference talks.

Extracts metadata (title, speaker, date, URL) without the full text,
creating a small file suitable for version control.
"""

import pandas as pd
from pathlib import Path

def generate_conference_metadata():
    """Extract metadata from conference talks CSV."""

    # Paths
    raw_path = Path(__file__).parent.parent / "data" / "raw" / "conference_talks.csv"
    metadata_path = Path(__file__).parent.parent / "data" / "metadata" / "conference_talks.csv"

    print(f"Reading talks from: {raw_path}")

    # Read full data
    df = pd.read_csv(raw_path)

    print(f"Loaded {len(df)} talks")

    # Extract metadata only (no full text)
    metadata = df[['title', 'speaker', 'href', 'date']].copy()

    # Add computed fields
    metadata['year'] = pd.to_datetime(metadata['date']).dt.year
    metadata['month'] = pd.to_datetime(metadata['date']).dt.month
    metadata['conference'] = metadata.apply(
        lambda row: f"{row['year']}-{'04' if row['month'] <= 6 else '10'}",
        axis=1
    )

    # Add word count from original
    metadata['word_count'] = df['text'].str.split().str.len()

    # Sort by date
    metadata = metadata.sort_values('date')

    # Save metadata
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata.to_csv(metadata_path, index=False)

    print(f"Saved metadata to: {metadata_path}")
    print(f"Metadata size: {metadata_path.stat().st_size / 1024:.1f} KB")
    print(f"Original size: {raw_path.stat().st_size / 1024 / 1024:.1f} MB")

    # Print summary
    print(f"\nSummary:")
    print(f"  Date range: {metadata['date'].min()} to {metadata['date'].max()}")
    print(f"  Conferences: {metadata['conference'].nunique()}")
    print(f"  Unique speakers: {metadata['speaker'].nunique()}")
    print(f"  Total talks: {len(metadata)}")

if __name__ == "__main__":
    generate_conference_metadata()

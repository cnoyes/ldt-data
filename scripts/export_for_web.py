#!/usr/bin/env python3
"""
Export data for web consumption.

Creates JSON files with aggregate statistics and sample data
suitable for serving via web apps.
"""

import pandas as pd
import json
from pathlib import Path
from collections import Counter

def export_conference_stats():
    """Export conference talk statistics for web."""

    # Paths
    metadata_path = Path(__file__).parent.parent / "data" / "metadata" / "conference_talks.csv"
    public_path = Path(__file__).parent.parent / "data" / "public"

    print(f"Reading metadata from: {metadata_path}")

    # Read metadata
    df = pd.read_csv(metadata_path)

    # Create public directory
    public_path.mkdir(parents=True, exist_ok=True)

    # 1. Overall statistics
    stats = {
        "total_talks": len(df),
        "date_range": {
            "start": df['date'].min(),
            "end": df['date'].max()
        },
        "conferences": df['conference'].nunique(),
        "speakers": df['speaker'].nunique(),
        "avg_word_count": int(df['word_count'].mean()),
        "total_words": int(df['word_count'].sum())
    }

    with open(public_path / "conference_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"✓ Exported conference_stats.json")

    # 2. Talks by year
    talks_by_year = df.groupby('year').agg({
        'title': 'count',
        'word_count': 'sum'
    }).rename(columns={'title': 'talk_count', 'word_count': 'total_words'})

    talks_by_year_data = {
        "years": talks_by_year.index.tolist(),
        "talk_counts": talks_by_year['talk_count'].tolist(),
        "total_words": talks_by_year['total_words'].tolist()
    }

    with open(public_path / "talks_by_year.json", 'w') as f:
        json.dump(talks_by_year_data, f, indent=2)
    print(f"✓ Exported talks_by_year.json")

    # 3. Top speakers (by talk count)
    top_speakers = df['speaker'].value_counts().head(20)
    top_speakers_data = {
        "speakers": top_speakers.index.tolist(),
        "talk_counts": top_speakers.values.tolist()
    }

    with open(public_path / "top_speakers.json", 'w') as f:
        json.dump(top_speakers_data, f, indent=2)
    print(f"✓ Exported top_speakers.json")

    # 4. Recent talks (last 10)
    df_sorted = df.sort_values('date', ascending=False)
    recent_talks = df_sorted.head(10)[['title', 'speaker', 'date', 'conference', 'href']].to_dict(orient='records')

    with open(public_path / "recent_talks.json", 'w') as f:
        json.dump(recent_talks, f, indent=2)
    print(f"✓ Exported recent_talks.json")

    # 5. Summary for README
    print(f"\n📊 Export Summary:")
    print(f"   Total talks: {len(df):,}")
    print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"   Conferences: {df['conference'].nunique()}")
    print(f"   Speakers: {df['speaker'].nunique()}")
    print(f"   Total words: {df['word_count'].sum():,}")

if __name__ == "__main__":
    export_conference_stats()

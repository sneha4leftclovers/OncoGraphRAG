"""
Build a NetworkX DiGraph from PrimeKG's kg.csv and save as GraphML for
fast reload in the pipeline.

PrimeKG's kg.csv columns (per the official repo/schema):
  relation, display_relation, x_index, x_id, x_type, x_name, x_source,
  y_index, y_id, y_type, y_name, y_source

We map: x_name --edge(relation=relation)--> y_name

Usage:
    python scripts/01_build_primekg_graph.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from onco_followup.config import settings  # noqa: E402


def build_graph(csv_path: Path, limit_rows: int | None = None) -> nx.DiGraph:
    print(f"Reading {csv_path} ...")
    df = pd.read_csv(csv_path, nrows=limit_rows)

    required_cols = {"x_name", "y_name", "relation"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"kg.csv is missing expected columns {missing}. "
            f"Found columns: {list(df.columns)}. "
            "If PrimeKG's schema changed, adjust the column mapping in this script."
        )

    g = nx.DiGraph()
    for row in tqdm(df.itertuples(index=False), total=len(df), desc="Building graph"):
        g.add_edge(row.x_name, row.y_name, relation=row.relation)

    print(f"Graph built: {g.number_of_nodes():,} nodes, {g.number_of_edges():,} edges")
    return g


def main():
    if not settings.primekg_csv.exists():
        print(
            f"PrimeKG CSV not found at {settings.primekg_csv}. "
            "Run scripts/00_download_primekg.py first."
        )
        sys.exit(1)

    g = build_graph(settings.primekg_csv)

    settings.primekg_graphml.parent.mkdir(parents=True, exist_ok=True)
    nx.write_graphml(g, settings.primekg_graphml)
    print(f"Saved graph to {settings.primekg_graphml}")


if __name__ == "__main__":
    main()

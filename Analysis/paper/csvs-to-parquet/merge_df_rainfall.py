from pathlib import Path
import pandas as pd

# Directory containing all pairwise product comparisons
base = Path("/gws/ssde/j25b/swift/mendrika/asnie/paper")

# Comparisons where the CSV files are organised as comparison/domain/product/
comparisons = [
    "core-vs-crr",
    "core-vs-roa",
    "rdt-vs-crr",
    "rdt-vs-roa",
    "ts-vs-crr",
    "ts-vs-roa",
]

# Geographic domains used in each comparison
domains = ["CA", "EA", "SA", "WA"]

for comparison in comparisons:
    comparison_path = base / comparison

    # Get the products present in this comparison
    # For example, core-vs-crr contains the products "core" and "crr"
    products = set()

    for domain in domains:
        domain_path = comparison_path / domain

        for product_path in domain_path.iterdir():
            if product_path.is_dir():
                products.add(product_path.name)

    # Merge all CSV files across CA, EA, SA and WA into one Parquet per product
    for product in sorted(products):
        dfs = []

        print(f"\nMerging {comparison} / {product}")

        for domain in domains:
            product_path = comparison_path / domain / product

            if not product_path.exists():
                continue

            # Each CSV corresponds to one observation time
            csv_files = sorted(product_path.glob("*.csv"))

            print(f"{domain}: {len(csv_files)} CSV files")

            for csv_file in csv_files:
                df = pd.read_csv(csv_file)

                # Convert the filename, e.g. 202403010015.csv, to an observation timestamp
                df["timestamp"] = pd.to_datetime(
                    csv_file.stem,
                    format="%Y%m%d%H%M",
                )

                # Keep track of the geographic domain after merging
                df["domain"] = domain

                dfs.append(df)

        if not dfs:
            continue

        # Concatenate every timestamp and domain for the current product
        merged = pd.concat(dfs, ignore_index=True)

        # Store the merged product at the comparison level
        # Example: core-vs-crr/core.parquet
        output_file = comparison_path / f"{product}.parquet"

        merged.to_parquet(
            output_file,
            index=False,
            engine="pyarrow",
        )

        print(f"Saved: {output_file}")
        print(f"Rows: {len(merged):,}")
from pathlib import Path

import pandas as pd


# Directory containing all pairwise product comparisons
base = Path("/gws/ssde/j25b/swift/mendrika/asnie/paper")

# LI comparisons include an additional threshold directory
comparisons = [
    "core-vs-li",
    "ts-vs-li",
]

# Geographic domains used in each comparison
domains = ["CA", "EA", "SA", "WA"]


for comparison in comparisons:
    comparison_path = base / comparison

    # Identify the two products included in the comparison
    # For example, core-vs-li contains "core" and "li"
    products = set()

    for domain in domains:
        domain_path = comparison_path / domain

        for product_path in domain_path.iterdir():
            if product_path.is_dir():
                products.add(product_path.name)

    # Create one Parquet file per product containing all domains and thresholds
    for product in sorted(products):
        dfs = []

        print(f"\nMerging {comparison} / {product}")

        for domain in domains:
            product_path = comparison_path / domain / product

            if not product_path.exists():
                continue

            # Threshold directories are 0, 0.032 and 1.056
            threshold_paths = sorted(
                path for path in product_path.iterdir()
                if path.is_dir()
            )

            for threshold_path in threshold_paths:
                threshold = float(threshold_path.name)

                # Each threshold directory contains individual timestamp CSV files
                csv_files = sorted(threshold_path.glob("*.csv"))

                print(
                    f"{domain} / threshold={threshold}: "
                    f"{len(csv_files)} CSV files"
                )

                for csv_file in csv_files:
                    df = pd.read_csv(csv_file)

                    # Extract the observation time from the CSV filename
                    df["timestamp"] = pd.to_datetime(
                        csv_file.stem,
                        format="%Y%m%d%H%M",
                    )

                    # Keep the geographic domain for filtering after merging
                    df["domain"] = domain

                    # Keep the threshold associated with these data
                    df["threshold"] = threshold

                    dfs.append(df)

        if not dfs:
            continue

        # Combine all timestamps, domains and thresholds for this product
        merged = pd.concat(dfs, ignore_index=True)

        # Save the complete product dataset at the comparison level
        # Example: core-vs-li/core.parquet
        output_file = comparison_path / f"{product}.parquet"

        merged.to_parquet(
            output_file,
            index=False,
            engine="pyarrow",
        )

        print(f"Saved: {output_file}")
        print(f"Rows: {len(merged):,}")
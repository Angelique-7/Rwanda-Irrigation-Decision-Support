
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

FILES = {
    "Irrigation": (
        OUTPUT_DIR
        / "cleaned_irrigation_methods_by_district.csv"
    ),
    "Water sources": (
        OUTPUT_DIR
        / "cleaned_irrigation_water_sources_by_district.csv"
    ),
}

METADATA = [
    "District",
    "Source_Table",
    "Season",
    "Category",
    "Data_Quality_Note",
]

for name, file_path in FILES.items():
    df = pd.read_csv(file_path)

    measures = [
        column for column in df.columns
        if column not in METADATA
    ]

    # Calculate totals only for rows with every measurement present.
    complete = df[measures].notna().all(axis=1)

    df["Percentage_Total"] = df[measures].sum(
        axis=1,
        min_count=len(measures),
    )

    print(f"\n{'=' * 60}")
    print(f"{name.upper()} — PERCENTAGE TOTALS")
    print("=" * 60)

    print("Complete rows:", int(complete.sum()))
    print("Incomplete rows:", int((~complete).sum()))

    if complete.any():
        totals = df.loc[complete, "Percentage_Total"]

        print("\nTotals for complete rows:")
        print(totals.describe().to_string())

        # Allow a small tolerance for rounding.
        outside_tolerance = ~totals.between(99.5, 100.5)

        print(
            "\nComplete rows outside 99.5%–100.5%:",
            int(outside_tolerance.sum()),
        )

        if outside_tolerance.any():
            print(
                df.loc[
                    totals.index[outside_tolerance],
                    ["District", "Season", "Percentage_Total"],
                ].to_string(index=False)
            )
    else:
        print(
            "\nNo complete rows are available for "
            "a full percentage-total check."
        )

    print(
        "\nNote: incomplete rows are not judged using "
        "partial totals."
    )

print("\nPercentage-total checks complete.")

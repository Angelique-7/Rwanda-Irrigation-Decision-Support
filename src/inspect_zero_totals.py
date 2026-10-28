
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

for name, file_path in FILES.items():
    df = pd.read_csv(file_path)

    metadata = [
        "District",
        "Source_Table",
        "Season",
        "Category",
        "Data_Quality_Note",
    ]

    measures = [
        col for col in df.columns
        if col not in metadata
    ]

    # Find rows where every measurement is present
    # and all reported measurements are zero.
    zero_rows = df[
        df[measures].notna().all(axis=1)
        & df[measures].eq(0).all(axis=1)
    ]

    print(f"\n{'=' * 60}")
    print(f"{name.upper()} — ALL-ZERO ROWS")
    print("=" * 60)

    if zero_rows.empty:
        print("No complete all-zero rows found.")
    else:
        print(
            zero_rows[
                ["District", "Season", "Source_Table"]
                + measures
            ].to_string(index=False)
        )

print("\nInspection complete.")

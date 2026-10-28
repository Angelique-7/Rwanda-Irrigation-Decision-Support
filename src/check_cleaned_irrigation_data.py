
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

files = {
    "Irrigation": (
        OUTPUT_DIR
        / "cleaned_irrigation_methods_by_district.csv"
    ),
    "Water sources": (
        OUTPUT_DIR
        / "cleaned_irrigation_water_sources_by_district.csv"
    ),
}

for name, file_path in files.items():
    df = pd.read_csv(file_path)

    print(f"\n{'=' * 55}")
    print(f"{name.upper()} — CLEANING CHECK")
    print("=" * 55)

    print(f"Dataset shape: {df.shape}")
    print(f"Unique districts: {df['District'].nunique()}")

    print("\nRows per season:")
    print(df.groupby("Season").size())

    measurement_columns = [
        column for column in df.columns
        if column not in [
            "District",
            "Source_Table",
            "Season",
            "Category",
            "Data_Quality_Note",
        ]
    ]

    print("\nMissing values by measurement:")
    print(df[measurement_columns].isna().sum())

    print("\nRows with missing measurements:")
    missing_rows = df[
        df[measurement_columns].isna().any(axis=1)
    ]

    print(
        missing_rows[
            ["District", "Season", "Source_Table"]
            + measurement_columns
        ].to_string(index=False)
    )

    print("\nDistrict names needing verification:")
    print(
        df[
            df["District"].str.contains(
                "Nyarugenege|Nyarugenge",
                case=False,
                na=False,
            )
        ][["District", "Season", "Source_Table"]]
        .to_string(index=False)
    )

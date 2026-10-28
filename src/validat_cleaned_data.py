
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
        column for column in df.columns
        if column not in metadata
    ]

    print(f"\n{'=' * 60}")
    print(f"{name.upper()} — FINAL VALIDATION")
    print("=" * 60)

    print("Dataset shape:", df.shape)
    print("Unique districts:", df["District"].nunique())
    print("Seasons:", sorted(df["Season"].dropna().unique()))

    print("\nRecords per season:")
    print(df.groupby("Season").size().to_string())

    print("\nMeasurement ranges:")
    print(
        df[measures]
        .agg(["min", "max"])
        .to_string()
    )

    print("\nValues outside the 0–100 percentage range:")
    for column in measures:
        invalid = df[
            df[column].notna()
            & ~df[column].between(0, 100)
        ]

        if invalid.empty:
            print(f"{column}: none")
        else:
            print(f"\n{column}:")
            print(
                invalid[
                    ["District", "Season", column]
                ].to_string(index=False)
            )

    print("\nNational rows accidentally included:")
    print(
        df[df["District"].str.lower().eq("national")]
        .shape[0]
    )

print("\nValidation complete.")

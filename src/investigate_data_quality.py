
from pathlib import Path
import pandas as pd

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

# Define the datasets and their percentage columns
datasets = {
    "cleaned_irrigation_methods_by_district.csv": [
        "Surface irrigation",
        "Flood irrigation",
        "Drip irrigation",
        "Sprinkler irrigation",
        "Pivot irrigation",
        "Traditional techniques",
    ],
    "cleaned_irrigation_water_sources_by_district.csv": [
        "Rainwater",
        "Water treatment",
        "Underground",
        "Lake / streams",
        "Water catchment",
    ],
}

# Inspect each dataset
for filename, percentage_columns in datasets.items():
    file_path = OUTPUT_DIR / filename
    data = pd.read_csv(file_path)

    # Calculate each row's total, preserving all-missing rows as missing
    data["Row_Total"] = data[percentage_columns].sum(
        axis=1,
        min_count=1,
    )

    # Identify rows with missing values or a zero total
    has_missing = data[percentage_columns].isna().any(axis=1)
    has_zero_total = data["Row_Total"].eq(0)
    rows_to_check = data[has_missing | has_zero_total]

    print("\n" + "=" * 65)
    print("DATASET:", filename)
    print("Rows requiring investigation:", len(rows_to_check))

    columns_to_show = [
        "District",
        "Season",
        *percentage_columns,
        "Row_Total",
    ]

    print(rows_to_check[columns_to_show].to_string(index=False))

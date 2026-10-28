
from pathlib import Path

import pandas as pd

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

# Input files
METHODS_FILE = OUTPUT_DIR / "cleaned_irrigation_methods_by_district.csv"
SOURCES_FILE = OUTPUT_DIR / "cleaned_irrigation_water_sources_by_district.csv"

# Load the cleaned datasets
methods = pd.read_csv(METHODS_FILE)
sources = pd.read_csv(SOURCES_FILE)

# Check whether District and Season uniquely identify each row
print("Duplicate district-season records in methods:",
      methods.duplicated(["District", "Season"]).sum())

print("Duplicate district-season records in sources:",
      sources.duplicated(["District", "Season"]).sum())

# Merge the two datasets using District and Season
combined = pd.merge(
    methods,
    sources,
    on=["District", "Season"],
    how="outer",
    suffixes=("_method", "_source"),
    validate="one_to_one",
)

# Save the combined dataset
output_file = OUTPUT_DIR / "combined_irrigation_data_by_district.csv"
combined.to_csv(output_file, index=False)

print(f"\nCombined dataset saved to: {output_file}")
print("Combined dataset shape:", combined.shape)

print("\nRecords per season:")
print(combined.groupby("Season")["District"].count())

print("\nFirst five rows:")
print(combined.head().to_string(index=False))

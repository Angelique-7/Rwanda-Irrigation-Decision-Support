
from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "combined_irrigation_data_by_district.csv"

data = pd.read_csv(DATA_FILE)

methods = [
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

sources = [
    "Rainwater",
    "Water treatment",
    "Underground",
    "Lake / streams",
    "Water catchment",
]

# Keep only records with at least one positive reported method.
method_values = data[methods]
valid_methods = (
    method_values.notna().any(axis=1)
    & method_values.fillna(0).sum(axis=1).gt(0)
)

# Keep only records with at least one positive reported water source.
source_values = data[sources]
valid_sources = (
    source_values.notna().any(axis=1)
    & source_values.fillna(0).sum(axis=1).gt(0)
)

# Calculate average reported percentages by district.
# Missing values are skipped; they are not replaced with zero.
method_profiles = (
    data.loc[valid_methods, ["District"] + methods]
    .groupby("District")[methods]
    .mean()
)

source_profiles = (
    data.loc[valid_sources, ["District"] + sources]
    .groupby("District")[sources]
    .mean()
)

# Count usable seasonal records for each district.
method_counts = (
    data.loc[valid_methods]
    .groupby("District")
    .size()
    .rename("Usable_Method_Seasons")
)

source_counts = (
    data.loc[valid_sources]
    .groupby("District")
    .size()
    .rename("Usable_Water_Source_Seasons")
)

# Combine the district summaries.
profiles = method_profiles.join(source_profiles, how="outer")
profiles = profiles.join(method_counts, how="left")
profiles = profiles.join(source_counts, how="left")

profiles = profiles.reset_index().sort_values("District")

output_file = OUTPUT_DIR / "district_irrigation_profiles.csv"
profiles.to_csv(output_file, index=False)

print(f"District profiles saved to: {output_file}")
print("\nTable shape:", profiles.shape)

print("\nFirst 10 district profiles:")
print(profiles.head(10).round(2).to_string(index=False))

print("\nNumber of usable method records per district:")
print(profiles["Usable_Method_Seasons"].value_counts().sort_index())

print("\nNumber of usable water-source records per district:")
print(
    profiles["Usable_Water_Source_Seasons"]
    .value_counts()
    .sort_index()
)

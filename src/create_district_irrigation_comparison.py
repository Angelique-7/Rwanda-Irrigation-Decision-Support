
from pathlib import Path

import pandas as pd

# Locate project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "combined_irrigation_data_by_district.csv"

# Load the combined dataset
data = pd.read_csv(DATA_FILE)

# Define the reported categories
methods = [
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

water_sources = [
    "Rainwater",
    "Water treatment",
    "Underground",
    "Lake / streams",
    "Water catchment",
]


def find_leading_category(row, categories):
    """Return the category with the highest positive reported value."""
    available = row[categories].dropna()

    if available.empty or available.max() <= 0:
        return pd.Series({
            "Leading_Category": "No positive reported value",
            "Leading_Percentage": float("nan"),
        })

    leader = available.idxmax()

    return pd.Series({
        "Leading_Category": leader,
        "Leading_Percentage": available[leader],
    })


# Prepare the comparison table
comparison = data[["District", "Season"]].copy()

# Find the leading irrigation method
method_results = data.apply(
    lambda row: find_leading_category(row, methods),
    axis=1,
)

comparison["Leading_Irrigation_Method"] = (
    method_results["Leading_Category"]
)
comparison["Method_Percentage"] = (
    method_results["Leading_Percentage"]
)

# Find the leading water source
source_results = data.apply(
    lambda row: find_leading_category(row, water_sources),
    axis=1,
)

comparison["Leading_Water_Source"] = (
    source_results["Leading_Category"]
)
comparison["Water_Source_Percentage"] = (
    source_results["Leading_Percentage"]
)


def record_status(row, categories):
    """Describe whether a record has usable reported values."""
    values = row[categories].dropna()

    if values.empty:
        return "No values reported"

    if values.max() <= 0:
        return "All reported values are zero"

    return "Positive reported values available"


comparison["Method_Data_Status"] = data.apply(
    lambda row: record_status(row, methods),
    axis=1,
)

comparison["Water_Source_Data_Status"] = data.apply(
    lambda row: record_status(row, water_sources),
    axis=1,
)

# Check whether the leading categories vary across seasons
# within each district, using only seasons with positive values.
for column, flag_name in [
    ("Leading_Irrigation_Method", "Method_Leader_Varies_Across_Seasons"),
    ("Leading_Water_Source", "Water_Source_Leader_Varies_Across_Seasons"),
]:
    valid_leaders = comparison[column].where(
        comparison[column] != "No positive reported value"
    )

    leader_counts = (
        comparison.assign(_leader=valid_leaders)
        .groupby("District")["_leader"]
        .nunique()
    )

    comparison[flag_name] = (
        comparison["District"]
        .map(leader_counts)
        .gt(1)
        .map({True: "Yes", False: "No"})
    )

# Arrange records consistently
comparison = comparison.sort_values(
    ["District", "Season"]
).reset_index(drop=True)

# Save the result
output_file = OUTPUT_DIR / "district_irrigation_comparison.csv"
comparison.to_csv(output_file, index=False)

print(f"Comparison table saved to: {output_file}")
print("\nTable shape:", comparison.shape)

print("\nFirst 10 rows:")
print(comparison.head(10).to_string(index=False))

print("\nMethod data status:")
print(comparison["Method_Data_Status"].value_counts())

print("\nWater-source data status:")
print(comparison["Water_Source_Data_Status"].value_counts())

print("\nDistricts where the leading method varies across seasons:")
print(
    comparison.loc[
        comparison["Method_Leader_Varies_Across_Seasons"] == "Yes",
        "District",
    ].drop_duplicates().to_list()
)

print("\nDistricts where the leading water source varies across seasons:")
print(
    comparison.loc[
        comparison["Water_Source_Leader_Varies_Across_Seasons"] == "Yes",
        "District",
    ].drop_duplicates().to_list()
)

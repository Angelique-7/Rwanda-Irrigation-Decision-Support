
from pathlib import Path
import pandas as pd

# 1. Locate the project and input file
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "cleaned_irrigation_water_sources_by_district.csv"

# 2. Load the cleaned dataset
data = pd.read_csv(DATA_FILE)

# 3. Identify the water-source columns
source_columns = [
    "Rainwater",
    "Water treatment",
    "Underground",
    "Lake / streams",
    "Water catchment",
]

# 4. Calculate the sum of reported percentages for each record
data["Row_Total"] = data[source_columns].sum(
    axis=1, min_count=1
)

# 5. Exclude district-season records with no usable
# distribution, including records where all values are zero
valid_data = data[
    data["Row_Total"].notna()
    & (data["Row_Total"] > 0)
].copy()

# 6. Calculate average reported percentages by season
average_percentages = (
    valid_data.groupby("Season")[source_columns]
    .mean()
)

# 7. Count districts where each source is dominant
dominant_sources = valid_data[source_columns].idxmax(axis=1)

dominant_counts = pd.crosstab(
    valid_data["Season"],
    dominant_sources
)

# 8. Display the results
print("\n" + "=" * 65)
print("AVERAGE REPORTED WATER-SOURCE PERCENTAGES")
print("=" * 65)
print(average_percentages.round(2).to_string())

print("\n" + "=" * 65)
print("NUMBER OF DISTRICTS WHERE EACH SOURCE IS DOMINANT")
print("=" * 65)
print(dominant_counts.to_string())

print("\nValid district records used:")
print(valid_data.groupby("Season")["District"].nunique())

# 9. Save the average percentages for later use
summary = (
    average_percentages
    .rename_axis("Season")
    .reset_index()
    .melt(
        id_vars="Season",
        var_name="Water_Source",
        value_name="Average_Percentage",
    )
)

summary["Average_Percentage"] = summary[
    "Average_Percentage"
].round(2)

summary.to_csv(
    OUTPUT_DIR / "water_sources_season_comparison.csv",
    index=False,
)

print("\nComparison summary saved successfully.")
print(
    OUTPUT_DIR / "water_sources_season_comparison.csv"
)

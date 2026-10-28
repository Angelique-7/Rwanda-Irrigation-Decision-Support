
from pathlib import Path
import pandas as pd

# 1. Locate the project and input file
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "cleaned_irrigation_methods_by_district.csv"

# 2. Load the cleaned dataset
data = pd.read_csv(DATA_FILE)

# 3. Identify the irrigation-method columns
method_columns = [
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

# 4. Keep only Seasons A and B
data = data[data["Season"].isin(["A", "B"])].copy()

# 5. Calculate the total reported percentage for each record
data["Row_Total"] = data[method_columns].sum(
    axis=1, min_count=1
)

# 6. Exclude records with missing totals or all-zero values
valid_data = data[
    data["Row_Total"].notna()
    & (data["Row_Total"] > 0)
].copy()

# 7. Calculate the average percentage for each method
# separately for Seasons A and B
average_percentages = (
    valid_data.groupby("Season")[method_columns]
    .mean()
)

# 8. Count how often each method is the dominant
# reported method across districts
dominant_methods = valid_data[method_columns].idxmax(axis=1)

dominant_counts = pd.crosstab(
    valid_data["Season"],
    dominant_methods
)

# 9. Display the results
print("\n" + "=" * 65)
print("AVERAGE IRRIGATION METHOD PERCENTAGES")
print("=" * 65)
print(average_percentages.round(2).to_string())

print("\n" + "=" * 65)
print("NUMBER OF DISTRICTS WHERE EACH METHOD IS DOMINANT")
print("=" * 65)
print(dominant_counts.to_string())

print("\nValid district records used:")
print(valid_data.groupby("Season")["District"].nunique())

# 10. Save the average percentages for later analysis
summary = (
    average_percentages
    .rename_axis("Season")
    .reset_index()
    .melt(
        id_vars="Season",
        var_name="Irrigation_Method",
        value_name="Average_Percentage",
    )
)

summary["Average_Percentage"] = summary[
    "Average_Percentage"
].round(2)

summary.to_csv(
    OUTPUT_DIR / "irrigation_methods_season_comparison.csv",
    index=False,
)

print("\nComparison summary saved successfully.")
print(
    OUTPUT_DIR / "irrigation_methods_season_comparison.csv"
)

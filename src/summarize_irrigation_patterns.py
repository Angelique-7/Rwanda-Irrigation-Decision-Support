
from pathlib import Path
import pandas as pd

# 1. Locate our project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

# 2. Define the columns we want to analyze
irrigation_methods = [
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


# 3. Summarize the reported categories in each row
def summarize_dataset(data, categories, dataset_type):
    results = []

    for _, row in data.iterrows():
        # Flood irrigation is not reported in Table 69 (Season C).
        reported_categories = categories.copy()

        if dataset_type == "methods" and row["Season"] == "C":
            reported_categories.remove("Flood irrigation")

        values = pd.to_numeric(
            row[reported_categories], errors="coerce"
        )

        available = values.dropna()
        row_total = available.sum()

        # Measure how much of the expected information is available.
        completeness = (
            len(available) / len(reported_categories) * 100
        )

        if available.empty:
            dominant = "No reported information"
        elif row_total == 0:
            dominant = "No positive values reported"
        else:
            dominant = available.idxmax()

        results.append({
            "District": row["District"],
            "Season": row["Season"],
            "Dominant_reported_category": dominant,
            "Available_categories": len(available),
            "Expected_categories": len(reported_categories),
            "Data_completeness_percent": round(completeness, 2),
            "Sum_of_reported_percentages": round(row_total, 2),
            "Has_missing_values": len(available) < len(reported_categories),
            "All_available_values_zero": (
                not available.empty and available.eq(0).all()
            ),
        })

    return pd.DataFrame(results)


# 4. Load the cleaned datasets
methods_file = OUTPUT_DIR / (
    "cleaned_irrigation_methods_by_district.csv"
)
sources_file = OUTPUT_DIR / (
    "cleaned_irrigation_water_sources_by_district.csv"
)

methods_data = pd.read_csv(methods_file)
sources_data = pd.read_csv(sources_file)

# 5. Analyze irrigation methods and water sources
methods_summary = summarize_dataset(
    methods_data, irrigation_methods, "methods"
)

sources_summary = summarize_dataset(
    sources_data, water_sources, "sources"
)

# 6. Save the results
methods_output = OUTPUT_DIR / "irrigation_patterns_summary.csv"
sources_output = OUTPUT_DIR / "water_sources_summary.csv"

methods_summary.to_csv(methods_output, index=False)
sources_summary.to_csv(sources_output, index=False)

# 7. Display initial findings
for title, summary in [
    ("IRRIGATION METHODS", methods_summary),
    ("IRRIGATION WATER SOURCES", sources_summary),
]:
    print("\n" + "=" * 65)
    print(title)
    print("=" * 65)

    print("\nRows analyzed by season:")
    print(summary.groupby("Season").size().to_string())

    print("\nData completeness by season (% of categories reported):")
    print(
        summary.groupby("Season")["Data_completeness_percent"]
        .mean()
        .round(2)
        .to_string()
    )

    print("\nDistrict-season records with all available values equal to zero:")
    zero_rows = summary[summary["All_available_values_zero"]]
    print(
        zero_rows[["District", "Season"]].to_string(index=False)
        if not zero_rows.empty
        else "None"
    )

print("\nAnalysis summaries saved successfully.")
print(methods_output)
print(sources_output)

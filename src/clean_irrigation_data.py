
from pathlib import Path
import pandas as pd

# Step 1: Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

# Step 2: Identify the original extracted CSV files
IRRIGATION_FILE = (
    OUTPUT_DIR / "irrigation_methods_by_district.csv"
)

WATER_FILE = (
    OUTPUT_DIR / "irrigation_water_sources_by_district.csv"
)

# Step 3: Define where the cleaned files will be saved
CLEAN_IRRIGATION_FILE = (
    OUTPUT_DIR / "cleaned_irrigation_methods_by_district.csv"
)

CLEAN_WATER_FILE = (
    OUTPUT_DIR / "cleaned_irrigation_water_sources_by_district.csv"
)

# Step 4: Check that both input files exist
for file_path in [IRRIGATION_FILE, WATER_FILE]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Required file not found: {file_path}"
        )


def clean_dataset(file_path, dataset_name):
    # Read the original extracted data
    df = pd.read_csv(file_path)
    # Standardize the verified district name
    df["District"] = df["District"].replace({
        "Nyarugenege": "Nyarugenge"
    })

    # Identify measurement columns, excluding metadata
    metadata_columns = [
        "District",
        "Source_Table",
        "Season",
        "Category",
    ]

    measurement_columns = [
        column
        for column in df.columns
        if column not in metadata_columns
    ]

    # Record where the original data contains dash symbols
    original_values = df[measurement_columns].copy()

    dash_mask = original_values.apply(
        lambda column: (
            column.astype("string")
            .str.strip()
            .isin(["-", "–", "—"])
        )
    )

    rows_with_dashes = dash_mask.any(axis=1)

    # Convert measurement columns to numeric values.
    # Dashes and other non-numeric entries become missing values.
    for column in measurement_columns:
        df[column] = pd.to_numeric(
            df[column]
            .astype("string")
            .str.strip()
            .replace(["-", "–", "—"], pd.NA),
            errors="coerce",
        )

    # Document data-quality issues without guessing their meaning
    notes = []

    for index, row in df.iterrows():
        row_notes = []

        if rows_with_dashes.loc[index]:
            row_notes.append(
                "Original dash(es) converted to missing; "
                "meaning not specified in source."
            )

        if df.loc[index, measurement_columns].isna().any():
            if not rows_with_dashes.loc[index]:
                row_notes.append(
                    "One or more measurements are missing."
                )

        # Flood irrigation was not included in Table 69
        if (
            dataset_name == "irrigation"
            and row["Source_Table"] == "Table 69"
        ):
            row_notes.append(
                "Flood irrigation not reported in Table 69."
            )

        notes.append(" ".join(row_notes))

    df["Data_Quality_Note"] = notes

    return df


# Step 5: Clean both datasets
irrigation = clean_dataset(
    IRRIGATION_FILE,
    "irrigation",
)

water = clean_dataset(
    WATER_FILE,
    "water",
)

# Step 6: Save cleaned data separately from the originals
irrigation.to_csv(CLEAN_IRRIGATION_FILE, index=False)
water.to_csv(CLEAN_WATER_FILE, index=False)

# Step 7: Print a summary for quality checking
for name, df, output_file in [
    ("IRRIGATION", irrigation, CLEAN_IRRIGATION_FILE),
    ("WATER SOURCES", water, CLEAN_WATER_FILE),
]:
    print(f"\n{'=' * 60}")
    print(f"{name} DATASET")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Unique districts: {df['District'].nunique()}")

    measurement_columns = [
        column
        for column in df.columns
        if column not in [
            "District",
            "Source_Table",
            "Season",
            "Category",
            "Data_Quality_Note",
        ]
    ]

    print("\nMissing measurements:")
    print(df[measurement_columns].isna().sum())

    print("\nRows with data-quality notes:")
    print(
        df["Data_Quality_Note"]
        .ne("")
        .sum()
    )

    print(f"\nSaved to: {output_file}")

print("\nCleaning completed.")

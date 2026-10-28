
from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Define project paths
# --------------------------------------------------

ProjectFolder = Path(__file__).resolve().parent.parent

DataFile = (
    ProjectFolder
    / "data"
    / "SAS 2025_Annual Tables - Cleaned one.xlsx"
)

OutputDir = ProjectFolder / "outputs"

OutputDir.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 2. Define the tables to extract
# --------------------------------------------------

TableConfig = {
    "Table 67": {
        "season": "A",
        "category": "irrigation_method",
        "first_data_row": 4,
        "expected_columns": 8,
    },
    "Table 68": {
        "season": "B",
        "category": "irrigation_method",
        "first_data_row": 4,
        "expected_columns": 8,
    },
    "Table 69": {
        "season": "C",
        "category": "irrigation_method",
        "first_data_row": 5,
        "expected_columns": 7,
    },
    "Table 70": {
        "season": "A",
        "category": "water_source",
        "first_data_row": 3,
        "expected_columns": 7,
    },
    "Table 71": {
        "season": "B",
        "category": "water_source",
        "first_data_row": 3,
        "expected_columns": 7,
    },
    "Table 72": {
        "season": "C",
        "category": "water_source",
        "first_data_row": 4,
        "expected_columns": 7,
    },
}


# --------------------------------------------------
# 3. Define standardized column names
# --------------------------------------------------

IRRIGATION_COLUMNS_AB = [
    "District",
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

IRRIGATION_COLUMNS_C = [
    "District",
    "Surface irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

WATER_SOURCE_COLUMNS = [
    "District",
    "Rainwater",
    "Water treatment",
    "Underground",
    "Lake / streams",
    "Water catchment",
]


# --------------------------------------------------
# 4. Define a reusable extraction function
# --------------------------------------------------

def extract_table(table_name, config):
    """Extract district-level records from one Excel table."""

    raw = pd.read_excel(
        DataFile,
        sheet_name=table_name,
        header=None,
        dtype=object,
        engine="openpyxl",
    )

    # Check the worksheet's original column count.
    if raw.shape[1] != config["expected_columns"]:
        raise ValueError(
            f"{table_name}: expected "
            f"{config['expected_columns']} columns, "
            f"but found {raw.shape[1]}."
        )

    # Select the correct column structure.
    if config["category"] == "irrigation_method":

        if table_name in ("Table 67", "Table 68"):
            columns = IRRIGATION_COLUMNS_AB

        elif table_name == "Table 69":
            columns = IRRIGATION_COLUMNS_C

        else:
            raise ValueError(
                f"Unexpected irrigation table: {table_name}"
            )

    elif config["category"] == "water_source":
        columns = WATER_SOURCE_COLUMNS

    else:
        raise ValueError(
            f"Unknown category: {config['category']}"
        )

    # Extract the data rows and remove the first Excel column.
    data = raw.iloc[config["first_data_row"]:].copy()
    data = data.iloc[:, 1:].copy()

    # Confirm that the extracted data matches the expected schema.
    if data.shape[1] != len(columns):
        raise ValueError(
            f"{table_name}: expected {len(columns)} data columns "
            f"after removing the first Excel column, "
            f"but found {data.shape[1]}."
        )

    # Assign standardized column names.
    data.columns = columns

    # Remove rows without district names.
    data = data[data["District"].notna()].copy()

    # Convert district labels to clean strings.
    data["District"] = (
        data["District"]
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------
    # IMPORTANT: Correct the district spelling
    # --------------------------------------------------

    # Standardize the known spelling inconsistency.
    # All other district labels and measurement values remain unchanged.
    data["District"] = data["District"].replace(
        {
            "Nyarugenege": "Nyarugenge",
        }
    )

    # Exclude national summaries and source notes.
    district_names = data["District"].str.lower()

    data = data[
        (district_names != "national")
        & (~district_names.str.startswith("source:"))
    ].copy()

    # Add metadata for traceability.
    data["Source_Table"] = table_name
    data["Season"] = config["season"]
    data["Category"] = config["category"]

    # Return the extracted table with a clean index.
    return data.reset_index(drop=True)


# --------------------------------------------------
# 5. Check that the source workbook exists
# --------------------------------------------------

if not DataFile.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DataFile}"
    )


# --------------------------------------------------
# 6. Extract all six tables
# --------------------------------------------------

extracted_tables = {}

for table_name, config in TableConfig.items():

    print(f"Extracting {table_name}...")

    extracted_tables[table_name] = extract_table(
        table_name,
        config,
    )


# --------------------------------------------------
# 7. Combine tables by category
# --------------------------------------------------

irrigation_data = pd.concat(
    [
        table
        for table in extracted_tables.values()
        if table["Category"].iloc[0] == "irrigation_method"
    ],
    ignore_index=True,
)

water_source_data = pd.concat(
    [
        table
        for table in extracted_tables.values()
        if table["Category"].iloc[0] == "water_source"
    ],
    ignore_index=True,
)


# --------------------------------------------------
# 8. Verify the district spelling before saving
# --------------------------------------------------

print("\n" + "=" * 65)
print("DISTRICT SPELLING VERIFICATION")
print("=" * 65)

incorrect_name = "Nyarugenege"
correct_name = "Nyarugenge"

for dataset_name, dataset in [
    ("Irrigation methods", irrigation_data),
    ("Water sources", water_source_data),
]:

    incorrect_count = (
        dataset["District"].eq(incorrect_name).sum()
    )

    correct_count = (
        dataset["District"].eq(correct_name).sum()
    )

    unique_districts = dataset["District"].nunique()

    print(f"\n{dataset_name}:")
    print(f"Remaining incorrect labels: {incorrect_count}")
    print(f"Rows labelled {correct_name}: {correct_count}")
    print(f"Unique district labels: {unique_districts}")

    if incorrect_count > 0:
        raise ValueError(
            f"Spelling correction failed in {dataset_name}: "
            f"{incorrect_count} incorrect labels remain."
        )

print("\nDistrict spelling verification passed.")


# --------------------------------------------------
# 9. Save the extracted datasets
# --------------------------------------------------

irrigation_file = (
    OutputDir / "irrigation_methods_by_district.csv"
)

water_file = (
    OutputDir / "irrigation_water_sources_by_district.csv"
)

irrigation_data.to_csv(
    irrigation_file,
    index=False,
)

water_source_data.to_csv(
    water_file,
    index=False,
)


# --------------------------------------------------
# 10. Print extraction summaries
# --------------------------------------------------

print("\n" + "=" * 65)
print("EXTRACTION SUMMARY")
print("=" * 65)

for table_name, table in extracted_tables.items():

    print(
        f"{table_name}: "
        f"{len(table)} district rows, "
        f"{table['District'].nunique()} unique district labels"
    )

print("\nCombined datasets:")

print(
    f"Irrigation methods: {len(irrigation_data)} rows"
)

print(
    f"Water sources: {len(water_source_data)} rows"
)

print("\nRecords per season:")

print("\nIrrigation methods:")
print(
    irrigation_data["Season"]
    .value_counts()
    .sort_index()
)

print("\nWater sources:")
print(
    water_source_data["Season"]
    .value_counts()
    .sort_index()
)

print("\nUnique district labels in the combined datasets:")
print(
    "Irrigation methods:",
    irrigation_data["District"].nunique(),
)

print(
    "Water sources:",
    water_source_data["District"].nunique(),
)

print("\nSaved files:")
print(irrigation_file)
print(water_file)

print("\nExtraction completed successfully.")

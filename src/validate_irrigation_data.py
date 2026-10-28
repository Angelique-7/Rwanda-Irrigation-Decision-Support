
from pathlib import Path
import pandas as pd

# Locate the project and output folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"
DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "SAS 2025_Annual Tables - Cleaned one.xlsx"
)

# Identify the two extracted datasets.
FILES = {
    "Irrigation methods": (
        OUTPUT_DIR / "irrigation_methods_by_district.csv"
    ),
    "Water sources": (
        OUTPUT_DIR / "irrigation_water_sources_by_district.csv"
    ),
}

# Inspect each dataset.
for dataset_name, file_path in FILES.items():
    print("\n" + "=" * 70)
    print(dataset_name.upper())
    print("=" * 70)

    # Confirm that the file exists.
    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find: {file_path}"
        )

    # Load the extracted CSV file.
    data = pd.read_csv(file_path)

    # Display its dimensions.
    print("\nShape (rows, columns):")
    print(data.shape)

    # Display column names.
    print("\nColumn names:")
    print(data.columns.tolist())

    # Display data types.
    print("\nData types:")
    print(data.dtypes)

    # Count missing values in each column.
    print("\nMissing values:")
    print(data.isna().sum())

    # Check unique district labels.
    print("\nNumber of unique districts:")
    print(data["District"].nunique())

    # Check the seasons represented.
    print("\nRecords per season:")
    print(data["Season"].value_counts().sort_index())

    # Display the first five records.
    print("\nFirst five records:")
    print(data.head().to_string(index=False))

print("\nValidation inspection completed.")


# Extra diagnostic checks for irrigation values
irrigation_file = OUTPUT_DIR / "irrigation_methods_by_district.csv"
irrigation = pd.read_csv(irrigation_file)

print("\n" + "=" * 70)
print("IRRIGATION VALUE DIAGNOSTICS")
print("=" * 70)

measurement_columns = [
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

print("\nRaw values from the first three records:")
print(
    irrigation[
        ["District", "Season"] + measurement_columns
    ].head(3).to_string(index=False)
)

print("\nData types of measurement columns:")
print(irrigation[measurement_columns].dtypes)

print("\nExamples of distinct values in each measurement column:")
for column in measurement_columns:
    print(f"\n{column}:")
    print(irrigation[column].dropna().unique()[:12])

print("\nRows with any missing irrigation measurements:")
print(
    irrigation.loc[
        irrigation[measurement_columns].isna().any(axis=1),
        ["District", "Season", "Source_Table"] + measurement_columns,
    ].to_string(index=False)
)


# Inspect the original Table 69 directly.
print("\n" + "=" * 70)
print("ORIGINAL TABLE 69: SOURCE CHECK")
print("=" * 70)

workbook = pd.ExcelFile(DATA_FILE, engine="openpyxl")

raw_table69 = pd.read_excel(
    workbook,
    sheet_name="Table 69",
    header=None,
    dtype=object,
)

print("\nHeader rows (Excel rows 1-6):")
print(raw_table69.iloc[0:6].to_string(index=True, header=False))

print("\nFinal rows (including national summary and notes):")
print(raw_table69.iloc[-6:].to_string(index=True, header=False))

print("\nExact cell values from the first district row:")
print([repr(value) for value in raw_table69.iloc[5].tolist()])


print("\n" + "=" * 70)
print("TABLE 69: DASH INTERPRETATION TEST")
print("=" * 70)

# Select the five irrigation-method columns.
# Rows 5–34 contain the 30 districts.
method_values = raw_table69.iloc[5:35, 2:7].copy()

# Temporarily treat dashes as zero for this diagnostic test.
# This does NOT change the saved dataset.
method_values = method_values.replace("-", 0)

# Convert the values to numbers for calculation.
method_values = method_values.apply(
    pd.to_numeric,
    errors="coerce"
)

# Calculate the total percentage across the five methods.
row_totals = method_values.sum(axis=1, min_count=1)

# Display the district and its calculated total.
dash_test = pd.DataFrame({
    "District": raw_table69.iloc[5:35, 1].values,
    "Percentage total": row_totals.values
})

print("\nDistrict percentage totals if dashes are zero:")
print(dash_test.to_string(index=False))

print("\nSummary of percentage totals:")
print(row_totals.describe())



print("\n" + "=" * 70)
print("DASH CHECK: SEASONS A AND B")
print("=" * 70)

for table_name in ["Table 67", "Table 68"]:
    raw_table = pd.read_excel(
        workbook,
        sheet_name=table_name,
        header=None,
        dtype=object,
    )

    print(f"\n{table_name}")

    # Find the row whose district label is National.
    district_labels = (
        raw_table.iloc[:, 1]
        .astype(str)
        .str.strip()
    )

    national_rows = raw_table.loc[
        district_labels.eq("National")
    ]

    print("\nNational summary row:")
    if national_rows.empty:
        print("National row not found.")
    else:
        print(national_rows.to_string(index=False, header=False))

    # Count dash entries in the 30 district rows.
    district_rows = raw_table.iloc[4:34, 2:8]

    dash_count = district_rows.apply(
        lambda column: column.astype(str).str.strip().eq("-")
    ).sum().sum()

    print(
        "\nNumber of dash entries in district data:",
        dash_count,
    )


# Inspect the original Season B table before cleaning
from pathlib import Path
import pandas as pd

project_dir = Path(__file__).resolve().parent.parent
excel_file = project_dir / "data" / "SAS 2025_Annual Tables - Cleaned one.xlsx"

table = pd.read_excel(
    excel_file,
    sheet_name="Table 68",
    header=None,
    engine="openpyxl",
)

print("\nORIGINAL TABLE 68: CHECK NYARUGENGE")
print(table[table.astype(str).apply(
    lambda row: row.str.contains(
        "Nyarugenge|Nyarugenege|National",
        case=False,
        regex=True
    ).any(),
    axis=1
)].to_string(index=False, header=False))

from pathlib import Path
import pandas as pd

# Locate the project folder
ProjectFolder = Path(__file__).resolve().parent.parent

# Locate the dataset
DataFile = (
    ProjectFolder
    / "data"
    / "SAS 2025_Annual Tables - Cleaned one.xlsx"
)

# Check whether the file exists
if not DataFile.exists():
    raise FileNotFoundError(
        f"Excel file not found: {DataFile}"
    )

# Read the workbook structure
excel_file = pd.ExcelFile(DataFile, engine="openpyxl")

print("Dataset loaded successfully!")
print(f"Workbook: {DataFile.name}")

print("\nWorksheets available:")

for sheet in excel_file.sheet_names:
    print("-", sheet)

print(f"\nTotal worksheets: {len(excel_file.sheet_names)}")


# Inspect the Contents worksheet
contents = pd.read_excel(
    DataFile,
    sheet_name="Contents",
    header=None
)

print("\nCONTENTS WORKSHEET")
print("-" * 50)
print(contents.to_string(index=False, header=False))


# Extract table titles from the Contents worksheet
table_titles = []

for value in contents.to_numpy().ravel():
    if pd.notna(value):
        title = str(value).strip()

        if title.lower().startswith("table "):
            table_titles.append(title)

print("\nALL TABLE TITLES")
print("-" * 70)

for title in table_titles:
    print(title)

# Search for topics relevant to our research
keywords = (
    "irrigation",
    "water",
    "soil",
    "erosion",
    "drought",
    "fertility",
    "rain"
)

print("\nPOTENTIALLY RELEVANT TABLES")
print("-" * 70)

for title in table_titles:
    if any(word in title.lower() for word in keywords):
        print(title)



# Inspect the structure and data quality of the irrigation tables

irrigation_sheets = [
    "Table 67",
    "Table 68",
    "Table 69",
    "Table 70",
    "Table 71",
    "Table 72",
]

for sheet in irrigation_sheets:
    table = pd.read_excel(
        DataFile,
        sheet_name=sheet,
        header=None,
        dtype=object
    )

    print("\n" + "=" * 80)
    print(f"INSPECTING {sheet}")
    print("=" * 80)

    # 1. Display the first six rows to identify titles and headers
    print("\nFIRST SIX ROWS:")
    print(table.head(6).to_string(index=True, header=False))

    # 2. Display the last four rows to identify national totals and notes
    print("\nLAST FOUR ROWS:")
    print(table.tail(4).to_string(index=True, header=False))

    # 3. Count missing cells and dash markers
    missing_cells = int(table.isna().sum().sum())
    dash_cells = int(
        table.map(
            lambda value: isinstance(value, str)
            and value.strip() == "-"
        ).sum().sum()
    )

    print("\nDATA-QUALITY SUMMARY:")
    print(f"Dimensions: {table.shape[0]} rows x {table.shape[1]} columns")
    print(f"Missing cells (NaN): {missing_cells}")
    print(f"Dash markers (-): {dash_cells}")

    # 4. Display district labels and other labels from column B
    if table.shape[1] > 1:
        print("\nLABELS IN COLUMN B:")
        print(table.iloc[:, 1].dropna().astype(str).to_list())

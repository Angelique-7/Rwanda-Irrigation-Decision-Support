
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_DIR
    / "data"
    / "SAS 2025_Annual Tables - Cleaned one.xlsx"
)

districts_to_check = ["Nyarugenge", "Nyabihu"]
tables_to_check = ["Table 68", "Table 71"]

for sheet_name in tables_to_check:
    df = pd.read_excel(
        DATA_FILE,
        sheet_name=sheet_name,
        header=None,
        engine="openpyxl",
    )

    print(f"\n{'=' * 65}")
    print(f"ORIGINAL WORKBOOK: {sheet_name}")
    print("=" * 65)

    for district in districts_to_check:
        matches = df.apply(
            lambda column: column.astype("string")
            .str.strip()
            .str.casefold()
            .eq(district.casefold())
        ).any(axis=1)

        print(f"\n{district}:")

        if matches.any():
            for index in df.index[matches]:
                print(f"Excel row: {index + 1}")
                print(
                    df.iloc[index]
                    .to_string()
                )
        else:
            print("District not found.")

print("\nSource inspection complete.")

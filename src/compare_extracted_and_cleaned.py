
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

file_pairs = [
    (
        "irrigation_methods_by_district.csv",
        "cleaned_irrigation_methods_by_district.csv",
        ["Nyabihu", "Nyarugenge"],
    ),
    (
        "irrigation_water_sources_by_district.csv",
        "cleaned_irrigation_water_sources_by_district.csv",
        ["Nyabihu", "Nyarugenge"],
    ),
]

for original_name, cleaned_name, districts in file_pairs:
    original = pd.read_csv(OUTPUT_DIR / original_name)
    cleaned = pd.read_csv(OUTPUT_DIR / cleaned_name)

    print("\n" + "=" * 65)
    print("ORIGINAL:", original_name)
    print("CLEANED:", cleaned_name)

    for district in districts:
        for season in ["A", "B", "C"]:
            print(f"\n{district} — Season {season}")

            for label, data in [
                ("Extracted", original),
                ("Cleaned", cleaned),
            ]:
                rows = data[
                    (data["District"] == district)
                    & (data["Season"] == season)
                ]

                print(f"\n{label}:")
                if rows.empty:
                    print("No matching row")
                else:
                    print(rows.to_string(index=False))

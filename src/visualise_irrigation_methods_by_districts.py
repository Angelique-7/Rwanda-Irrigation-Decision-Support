
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "cleaned_irrigation_methods_by_district.csv"

# Load the cleaned irrigation-methods data
data = pd.read_csv(DATA_FILE)

# Irrigation methods reported in the dataset
methods = [
    "Surface irrigation",
    "Flood irrigation",
    "Drip irrigation",
    "Sprinkler irrigation",
    "Pivot irrigation",
    "Traditional techniques",
]

# Season C does not report Flood irrigation.
# Therefore, exclude that column only when plotting Season C.
fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(20, 12),
    sharey=True,
)

for ax, season in zip(axes, ["A", "B", "C"]):
    season_data = data[data["Season"] == season].copy()

    # Exclude records with no reported irrigation-method values.
    available_methods = [
        method for method in methods
        if method in season_data.columns
        and not (season == "C" and method == "Flood irrigation")
    ]

    # Remove districts where all available method values are missing
    season_data = season_data.dropna(
        subset=available_methods,
        how="all",
    )

    # Remove records where every reported method percentage is zero.
    # Individual zero values remain valid.
    season_data = season_data[
        season_data[available_methods].fillna(0).sum(axis=1) > 0
    ]

    heatmap_data = season_data.set_index("District")[available_methods]

    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1f",
        cmap="YlGnBu",
        vmin=0,
        vmax=100,
        linewidths=0.3,
        ax=ax,
        cbar=(season == "C"),
    )

    ax.set_title(f"Season {season}")
    ax.set_xlabel("Irrigation method")
    ax.set_ylabel("District" if season == "A" else "")
    ax.tick_params(axis="y", labelsize=7)
    ax.tick_params(axis="x", rotation=45)

fig.suptitle(
    "Reported Irrigation Methods by District and Season",
    fontsize=15,
)

plt.tight_layout()

# Save the heatmap
chart_path = OUTPUT_DIR / "irrigation_methods_by_district_heatmap.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Chart saved to: {chart_path}")

print("\nDistrict records included in each season:")
print(data.groupby("Season")["District"].count())

print("\nRecords with at least one reported, positive method percentage:")
for season in ["A", "B", "C"]:
    season_data = data[data["Season"] == season].copy()

    available_methods = [
        method for method in methods
        if method in season_data.columns
        and not (season == "C" and method == "Flood irrigation")
    ]

    valid = season_data.dropna(subset=available_methods, how="all")
    valid = valid[valid[available_methods].fillna(0).sum(axis=1) > 0]

    print(f"Season {season}: {len(valid)} districts")


from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "cleaned_irrigation_water_sources_by_district.csv"

# Load the cleaned data
data = pd.read_csv(DATA_FILE)

# Select the water-source columns
water_sources = [
    "Rainwater",
    "Water treatment",
    "Underground",
    "Lake / streams",
    "Water catchment",
]

# Exclude district-season records with missing values
# or with all water-source percentages equal to zero.
# Individual zero percentages remain valid.
valid_data = data.dropna(subset=water_sources).copy()

valid_data["Total_Percentage"] = valid_data[water_sources].sum(axis=1)

valid_data = valid_data[valid_data["Total_Percentage"] > 0]

# Create a separate heatmap for each season
fig, axes = plt.subplots(
    nrows=1,
    ncols=3,
    figsize=(18, 12),
    sharey=True,
)

for ax, season in zip(axes, ["A", "B", "C"]):
    season_data = valid_data[valid_data["Season"] == season]

    heatmap_data = season_data.set_index("District")[water_sources]

    # Keep districts in their original dataset order
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
    ax.set_xlabel("Water source")
    ax.set_ylabel("District" if season == "A" else "")
    ax.tick_params(axis="y", labelsize=7)
    ax.tick_params(axis="x", rotation=45)

fig.suptitle(
    "Reported Irrigation Water Sources by District and Season",
    fontsize=15,
)

plt.tight_layout()

# Save the chart
chart_path = OUTPUT_DIR / "water_sources_by_district_heatmap.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print(f"Chart saved to: {chart_path}")
print("\nValid district-season records:")
print(valid_data.groupby("Season")["District"].count())

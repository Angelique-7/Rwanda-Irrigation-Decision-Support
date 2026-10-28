
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# Locate the project files
PROJECT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_DIR / "outputs"

DATA_FILE = OUTPUT_DIR / "water_sources_season_comparison.csv"

# Load the summary we already calculated
data = pd.read_csv(DATA_FILE)

# Reshape the data for a grouped bar chart
chart_data = data.pivot(
    index="Water_Source",
    columns="Season",
    values="Average_Percentage",
)

# Arrange the seasons in the correct order
chart_data = chart_data[["A", "B", "C"]]

# Create the chart
ax = chart_data.plot(
    kind="bar",
    figsize=(11, 6),
    width=0.8,
)

ax.set_title(
    "Average Reported Irrigation Water Sources by Season"
)
ax.set_xlabel("Water source")
ax.set_ylabel("Average reported percentage (%)")
ax.legend(title="Agricultural season")
ax.tick_params(axis="x", rotation=25)

plt.tight_layout()

# Save the chart
chart_path = OUTPUT_DIR / "water_sources_by_season.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Chart saved to: {chart_path}")

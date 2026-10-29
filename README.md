# Rwanda Irrigation Decision Support System

A professional, data-driven Streamlit application for exploring irrigation methods and agricultural water sources across Rwanda's districts to support climate-resilient agricultural planning.

## 🎯 Overview

This application analyzes data from the National Institute of Statistics of Rwanda (NISR) Seasonal Agricultural Survey (SAS) 2025 to provide insights on:
- Irrigation methods used across districts and agricultural seasons
- Agricultural water sources and their distribution
- Data-informed intervention recommendations for irrigation improvements
- Water storage and management strategies

## 🚀 Features

- **🏠 Home Dashboard** - Overview of the system with key statistics
- **🗺️ District Explorer** - Detailed analysis of irrigation patterns by district and season with interactive visualizations
- **🎯 Intervention Planner** - Smart recommendations for irrigation improvements and water storage solutions
- **📋 About the Data** - Comprehensive information about data sources, methodology, and limitations

## 📊 Data

The application uses cleaned datasets from NISR SAS 2025:
- `cleaned_irrigation_methods_by_district.csv` - Irrigation methods by district and season
- `cleaned_irrigation_water_sources_by_district.csv` - Water sources by district and season

## 🛠️ Installation & Usage

### Prerequisites
- Python 3.8+
- pip

### Setup
1. Clone the repository
```bash
git clone <repository-url>
cd Rwanda-Irrigation-Decision-Support
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
Rwanda-Irrigation-Decision-Support/
├── app.py                      # Main application entry point
├── pages/                      # Multi-page application
│   ├── 1_🗺️_District_Explorer.py
│   ├── 2_🎯_Intervention_Planner.py
│   └── 3_📋_About_the_Data.py
├── Outputs/                    # Cleaned datasets and visualizations
├── data/                       # Raw data files
├── src/                        # Data processing scripts
└── requirements.txt            # Python dependencies
```

## ⚠️ Important Notes

- This tool provides **planning support only** - recommendations are based on reported patterns, not direct measurements of water stress
- Additional local assessment is essential before implementing any interventions
- Missing values are preserved (not treated as zeros) to maintain data integrity
- Season C has limited data availability - interpret with caution

## 🏆 NISR Big Data Hackathon 2026

**Track:** Agricultural Productivity  
**Goal:** Data-driven exploration for climate-resilient agricultural planning in Rwanda

---

*Built with ❤️ for sustainable agriculture in Rwanda*

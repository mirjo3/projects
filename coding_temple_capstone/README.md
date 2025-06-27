# Medicare Opioid Treatment Program Analysis

Python and Tableau project analyzing Medicare opioid treatment program distribution across the United States. Combines government treatment center data with census demographics to identify underserved regions.

## Overview

Analyzes geographic distribution of Medicare-funded opioid treatment programs to identify areas lacking adequate treatment access. Uses per capita analysis to highlight regions where federal investment could improve treatment availability.

**Key Features:**
- API integration with government datasets
- Geographic analysis by state and region
- Per capita treatment ratio calculations
- Interactive dashboard for policy planning

## Data Sources

- **Primary:** [CMS Opioid Treatment Program Providers](https://data.cms.gov/provider-characteristics/medicare-provider-supplier-enrollment/opioid-treatment-program-providers)
- **Secondary:** US Census demographic data
- **Method:** Python API integration for automated data retrieval

## Methodology

### 1. Data Collection
- Retrieved treatment center locations via CMS API
- Collected state population data from census sources
- Automated data refresh process using Python

### 2. Geographic Analysis
- Mapped treatment centers by state and region
- Calculated treatment centers per capita by state
- Identified geographic gaps in coverage

### 3. Visualization
- Built interactive Tableau dashboard
- Created state-by-state comparison charts
- Developed per capita treatment ratio maps

## Key Findings

**Treatment Distribution:**
- Significant variation in per capita treatment availability
- Rural states show lower treatment center density
- Geographic clusters in urban areas

**Policy Implications:**
- Identified underserved regions for targeted investment
- Quantified treatment gaps for federal planning
- Provided data foundation for resource allocation

## Tableau Dashboard

[**View Interactive Dashboard**](https://public.tableau.com/views/OpioidTreatmentProgramsintheUS/cms_participants?:language=en-US&:display_count=n&:origin=viz_share_link)

Features:
- State-by-state treatment center counts
- Per capita analysis with population weighting
- Geographic heat maps showing coverage gaps
- Filterable by region and demographics

## Technologies

- **Python:** Pandas, Requests (API integration), data processing
- **Tableau:** Interactive dashboards, geographic mapping
- **APIs:** CMS Provider API, Census demographic data
- **Analysis:** Statistical comparison, per capita calculations

## Business Impact

- **Policy Planning:** Identifies priority regions for federal investment
- **Resource Allocation:** Data-driven approach to treatment center placement
- **Gap Analysis:** Quantifies underserved populations by geography
- **Cost Optimization:** Targets areas with highest need-to-resource ratios

## Project Structure
```
medicare-opioid-analysis/
├── data_collection.py          # API data retrieval
├── data_processing.py          # Cleaning and analysis
├── analysis_output.csv         # Processed results
├── tableau_dashboard.twb       # Interactive visualizations
└── README.md                   # Documentation
```
## Usage

### Prerequisites
```bash
pip install pandas requests
```
Data Collection
```
import requests
import pandas as pd

# CMS API endpoint
dataset_id = "f1a8c197-b53d-4c24-9770-aea5d5a97dfb"
url = f"https://data.cms.gov/data-api/v1/dataset/{dataset_id}/data"

# Get data from API
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)
```
Data Processing
```
# Clean column names
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Split multiple NPI values into separate rows
df['npi'] = df['npi'].str.split(' ')
df = df.explode('npi').reset_index(drop=True)

# Export for visualization
df.to_csv('opioid_providers.csv', index=False)
```
Run Complete Analysis
```
# Clone repository
git clone [your-repo-url]

# Run Jupyter notebook
jupyter notebook cmsdata.ipynb

# Or run as Python script
python data_collection.py
```
Output Files:

opioid_providers.csv - Cleaned provider data ready for Tableau
Analysis summary with provider counts by state

Geographic distribution data for mapping

## Future Enhancements

Real-time Updates: Automated monthly data refresh

Demographic Overlay: Income and insurance coverage analysis

Trend Analysis: Multi-year comparison of program growth

Cost Analysis: Integration with program funding data

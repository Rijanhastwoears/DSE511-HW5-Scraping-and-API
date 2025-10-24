# Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

# Homework Specific notes
**Option choice**: I chose option one.

**Data**: The data I chose is coming from the [Federal Reserve's API](https://fred.stlouisfed.org/docs/api/fred/). 

**Reproduction**: To reproduce the workflow please go to the [usage](##Usage) section of this readme.

**Limitation**: The only limiation is that you will need an API key.

## Ethics Reflection

The best I can tell FREDAPI (the Federal Reserve's API) has only one condition: proper attribution. 

Said proper attribution needs to look something like this:

> Source: U.S. Bureau of Labor Statistics, retrieved from FRED, Federal Reserve Bank of St. Louis.

It is worth noting that while the data is coming from an independent branch of the US government it does not come attached with a warranty or endorsement.

I don't think there are any particular dangers to this type of data or using this API.

The following soruces should have more details on this:

- **FRED API Home**: [https://fred.stlouisfed.org/docs/api/fred/](https://fred.stlouisfed.org/docs/api/fred/)
- **Terms of Use**: [https://www.stlouisfed.org/terms-of-use](https://www.stlouisfed.org/terms-of-use)

# Mini-Analysis:

There are two ways to access the Mini-Analysis:

- Run the reproduction script named `income_unemployment_analysis.py`

- Or visit this [Onedrive link](https://liveutk-my.sharepoint.com/:f:/g/personal/rdhakal2_vols_utk_edu/EgFnqokHHONHvY1J8WiEYGsBZGZpEo_gMNTowiHqqZ6BMg?e=OZfP8I)

# Economic Data Analysis with FRED API

A comprehensive Python toolkit for retrieving and analyzing economic data from the Federal Reserve Economic Data (FRED) API. This project provides tools to fetch unemployment rate data, perform demographic analysis, generate visualizations, and create statistical reports.

## Project Overview

This repository contains Python scripts that leverage the FRED API to analyze unemployment trends across different economic and demographic dimensions. The project includes:

- **FRED API Client**: A robust client for searching, retrieving, and processing economic time series data
- **Unemployment Analysis**: Scripts for analyzing various unemployment rate categories and demographic breakdowns
- **Data Visualization**: Academic-style charts and trend analysis
- **Statistical Reporting**: Automated generation of summary statistics and insights



## Features

- 🔍 **Data Retrieval**: Fetch historical economic data from FRED API with customizable date ranges
- 📊 **Demographic Analysis**: Analyze unemployment rates by race, gender, age, and economic class
- 📈 **Visualizations**: Create publication-quality trend charts using matplotlib and seaborn
- 📋 **Statistical Reports**: Generate comprehensive summary statistics and key insights
- 💾 **Data Management**: Automatic saving of raw and cleaned data to organized directories
- 🔧 **Flexible Cleaning**: Multiple methods for handling missing data (drop, forward-fill, interpolate)

## Installation

### Prerequisites

- Python 3.12 or higher
- A free FRED API key (get one at: https://fred.stlouisfed.org/docs/api/api_key.html)

### Using uv (Recommended)

This project uses modern Python packaging with `uv`. If you don't have `uv` installed:

**On macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**On Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.sh | iex"
```

Then install dependencies:
```bash
uv sync
```

### Alternative: Using pip

If you prefer not to use `uv`, you can install dependencies with pip:

```bash
pip install -r requirements.txt
```

Note: The `requirements.txt` may not include all optional dependencies used in the analysis scripts (like matplotlib and seaborn). For full functionality, install from `pyproject.toml`:

```bash
pip install -e .
```

## Configuration

1. **Set your FRED API Key**: Open `fred_client.py` and replace the placeholder on line 7:

Note for Scott:- I have put my API keyh in the script - probably should not do that but it does save you some time :).
   ```python
   API_KEY = 'your-actual-api-key-here'
   ```

## Project Structure

```
├── fred_client.py              # Core FRED API client module
├── unemployment_analysis.py    # Analysis of different unemployment categories
├── income_unemployment_analysis.py  # Demographic unemployment analysis
├── main.py                     # Simple project entry point
├── pyproject.toml             # Modern Python project configuration
├── requirements.txt           # Legacy requirements file
├── uv.lock                    # uv package lock file
├── raw_data/                  # Directory for raw data files
├── clean_data/                # Directory for cleaned data files
└── reports/                   # Analysis outputs and reports
    └── income_analysis/       # Income-specific analysis outputs
```

## Usage
This section has a script that should show a reproducible workflow that uses the logic in this code.

### Running the Income Unemployment Analysis

The `income_unemployment_analysis.py` script analyzes unemployment rates across different demographic groups (race, gender, age, marital status).

#### Basic Usage

To run the analysis with default settings (last 10 years):

```bash
python income_unemployment_analysis.py
```

#### What the Script Does

1. **Data Retrieval**: Fetches unemployment data for 10 demographic groups from FRED
2. **Visualization**: Creates a 4-panel chart showing trends across:
   - Racial/Ethnic groups (White, Black, Hispanic, Asian)
   - Gender groups (Men 20+, Women, Married men, Women maintaining families)
   - Age groups (16-19, 20+)
   - Combined trends with 12-month rolling averages
3. **Statistics**: Generates descriptive statistics including mean, median, volatility, and 10-year changes
4. **Reporting**: Saves all outputs to the `reports/income_analysis/` directory

#### Output Files Generated

- `income_unemployment_statistics.csv`: Summary statistics for all demographic groups
- `income_unemployment_trends.png`: Academic-style trend visualization
- Individual CSV files for each demographic group's raw data

#### Customization

You can modify the analysis by editing the script:

- **Change time period**: Modify `years_back` parameter in `get_income_unemployment_data()` (default: 10)
- **Add/remove groups**: Update the `income_unemployment_series` dictionary with different FRED series IDs
- **Adjust visualization**: Modify chart parameters in `create_income_trend_visualization()`


#### Using the FRED Client Directly

```bash
python fred_client.py
```

This runs examples demonstrating:
- Searching for economic series
- Retrieving time series data
- Data cleaning and saving
- Metadata access

## API Reference

### FRED Client Functions

- `search_series(keyword, category, limit)`: Search for economic data series
- `get_series_data(series_id, start_date, end_date, frequency, units)`: Retrieve time series data
- `get_series_info(series_id)`: Get metadata about a dataset
- `clean_data(df, method)`: Clean data using different methods (drop, forward_fill, interpolate, zero)
- `save_data(df, series_id, raw, format)`: Save data to raw_data/ or clean_data/ directories

### Analysis Functions

- `get_unemployment_data(years_back)`: Retrieve unemployment data for different categories
- `get_income_unemployment_data(years_back)`: Retrieve unemployment data by demographic groups
- `create_trend_visualization(data_dict, save_path)`: Generate trend charts
- `generate_descriptive_stats(data_dict)`: Calculate summary statistics
- `create_summary_report(data_dict, save_dir)`: Generate complete analysis reports

## Data Sources

All data is retrieved from the **Federal Reserve Bank of St. Louis FRED® API**.

## Examples

See the `if __name__ == "__main__"` sections in each script for usage examples.

## Requirements

- Python 3.12+
- fredapi
- pandas
- requests
- matplotlib
- seaborn

## Support

For issues related to:
- FRED API access: Visit https://fred.stlouisfed.org/docs/api/api_key.html
- Python dependencies: Check `pyproject.toml` for version requirements
- Data analysis questions: Refer to FRED documentation for series definitions
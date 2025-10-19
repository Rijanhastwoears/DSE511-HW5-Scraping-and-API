# FRED API Client

A Python program to interact with the Federal Reserve Economic Data (FRED) API.

## Features

- Search for economic data series by keywords or categories
- Retrieve time series data with customizable date ranges
- Access metadata about datasets
- Support for multiple data formats (pandas DataFrames, JSON, XML)
- Filter data by various criteria

## Installation

1. Install dependencies:
   ```
   uv install
   ```

2. Set your FRED API key in `fred_client.py`:
   ```python
   API_KEY = 'your-api-key-here'
   ```

## Usage

Run the script to see examples:
```bash
python fred_client.py
```

### Functions

- `search_series(keyword, category, limit)`: Search for series
- `get_series_data(series_id, start_date, end_date, frequency, units)`: Retrieve data
- `get_series_info(series_id)`: Get metadata
- `get_data_as_json(series_id, start_date, end_date)`: Get data in JSON format

## Examples

See the `if __name__ == "__main__"` section in `fred_client.py` for usage examples including:
- Searching for GDP data
- Retrieving unemployment rates
- Getting metadata
- Filtering by categories

## API Key

Get your free API key from: https://fred.stlouisfed.org/docs/api/api_key.html
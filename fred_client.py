import pandas as pd
from fredapi import Fred
import os
import json

# Set your FRED API key here
API_KEY = 'a32eb6d579c4c29969e2e25c1ca62716'

# Initialize the FRED client
fred = Fred(api_key=API_KEY)

def ensure_directories():
    """
    Ensure that raw_data and clean_data directories exist.
    """
    os.makedirs('raw_data', exist_ok=True)
    os.makedirs('clean_data', exist_ok=True)

def search_series(keyword=None, category=None, limit=10):
    """
    Search for economic data series by keywords or categories.

    Parameters:
    keyword (str): Search term (e.g., 'GDP', 'unemployment')
    category (str): Category filter (e.g., 'Production & Business Activity')
    limit (int): Number of results to return

    Returns:
    pandas.DataFrame: Search results with series information
    """
    try:
        results = fred.search(keyword, limit=limit)
        if category:
            # Filter by category if specified (rough match)
            results = results[results['notes'].str.contains(category, case=False, na=False)]
        return results[['id', 'title', 'units', 'frequency', 'seasonal_adjustment', 'last_updated', 'observation_start', 'observation_end']]
    except Exception as e:
        print(f"Error searching series: {e}")
        return None

def get_series_data(series_id, start_date=None, end_date=None, frequency=None, units=None):
    """
    Retrieve time series data for a specific economic indicator.

    Parameters:
    series_id (str): The series ID (e.g., 'GDP', 'UNRATE')
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    frequency (str): Data frequency ('d', 'w', 'm', 'q', 'a')
    units (str): Units transformation ('lin', 'chg', 'ch1', 'pch', 'pc1', 'pca', 'cch', 'cca', 'log')

    Returns:
    pandas.DataFrame: Time series data
    """
    try:
        # Only pass non-None parameters to avoid API errors
        kwargs = {}
        if start_date:
            kwargs['observation_start'] = start_date
        if end_date:
            kwargs['observation_end'] = end_date
        if frequency:
            kwargs['frequency'] = frequency
        if units:
            kwargs['units'] = units
        data = fred.get_series(series_id, **kwargs)
        return pd.DataFrame(data, columns=[series_id])
    except Exception as e:
        print(f"Error retrieving data for {series_id}: {e}")
        return None

def clean_data(df, method='drop'):
    """
    Clean FRED data by handling missing values.

    Parameters:
    df (pandas.DataFrame): The data to clean
    method (str): Cleaning method - 'drop', 'forward_fill', 'interpolate', 'zero'

    Returns:
    pandas.DataFrame: Cleaned data
    """
    if method == 'drop':
        return df.dropna()
    elif method == 'forward_fill':
        return df.fillna(method='ffill')
    elif method == 'interpolate':
        return df.interpolate()
    elif method == 'zero':
        return df.fillna(0)
    else:
        raise ValueError("Method must be 'drop', 'forward_fill', 'interpolate', or 'zero'")

def save_data(df, series_id, raw=True, format='csv'):
    """
    Save data to file in the appropriate directory.

    Parameters:
    df (pandas.DataFrame): Data to save
    series_id (str): Series identifier for filename
    raw (bool): If True, save to raw_data/; if False, save to clean_data/
    format (str): File format - 'csv' or 'json'
    """
    # Ensure directories exist
    ensure_directories()

    if raw:
        directory = 'raw_data'
        filename = f'{series_id}_raw.{format}'
    else:
        directory = 'clean_data'
        filename = f'{series_id}_cleaned.{format}'

    filepath = os.path.join(directory, filename)

    try:
        if format == 'csv':
            df.to_csv(filepath)
        elif format == 'json':
            df.to_json(filepath, orient='records', date_format='iso')
        print(f"Data saved to {filepath}")
    except Exception as e:
        print(f"Error saving data to {filepath}: {e}")

def get_series_info(series_id):
    """
    Access metadata about a specific dataset.

    Parameters:
    series_id (str): The series ID

    Returns:
    dict: Series metadata
    """
    try:
        info = fred.get_series_info(series_id)
        return info.to_dict()
    except Exception as e:
        print(f"Error retrieving info for {series_id}: {e}")
        return None

def get_data_as_json(series_id, start_date=None, end_date=None):
    """
    Retrieve data in JSON format (using requests for raw JSON).

    Note: fredapi returns pandas DF, but for JSON, we can use the API directly.
    This is a basic implementation; in practice, use fredapi for ease.
    """
    import requests

    base_url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={API_KEY}&file_type=json"
    if start_date:
        base_url += f"&observation_start={start_date}"
    if end_date:
        base_url += f"&observation_end={end_date}"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving JSON data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Example 1: Search for GDP data
    print("Searching for GDP series...")
    gdp_search = search_series(keyword='GDP')
    print(gdp_search.head())

    # Example 2: Get GDP data
    print("\nRetrieving GDP data...")
    gdp_data = get_series_data('GDP', start_date='2020-01-01', end_date='2023-01-01')
    if gdp_data is not None:
        print("Raw data:")
        print(gdp_data.head())
        
        # Save raw data
        save_data(gdp_data, 'GDP', raw=True)
        
        # Clean the data
        cleaned_data = clean_data(gdp_data, method='drop')
        print(f"\nAfter cleaning (dropped NAs): {len(cleaned_data)} rows")
        print(cleaned_data.head())
        
        # Save cleaned data
        save_data(cleaned_data, 'GDP', raw=False)
    else:
        print("Failed to retrieve GDP data.")

    # Example 3: Get series metadata
    print("\nGetting metadata for GDP...")
    gdp_info = get_series_info('GDP')
    print(gdp_info)

    # Example 4: Get data in JSON format
    print("\nRetrieving GDP data as JSON...")
    gdp_json = get_data_as_json('GDP', start_date='2020-01-01', end_date='2023-01-01')
    if gdp_json:
        print(json.dumps(gdp_json, indent=2)[:500])  # Print first 500 chars
    else:
        print("Failed to retrieve JSON data.")

    # Example 5: Search with category filter
    print("\nSearching for unemployment data in Labor Markets...")
    unemp_search = search_series(keyword='unemployment', category='Labor Markets')
    print(unemp_search.head())

    # Example 6: Get unemployment rate data
    print("\nRetrieving unemployment rate data...")
    unrate_data = get_series_data('UNRATE', start_date='2020-01-01', end_date='2023-01-01')
    if unrate_data is not None:
        print("Raw data:")
        print(unrate_data.head())
        
        # Save raw data
        save_data(unrate_data, 'UNRATE', raw=True)
        
        # Clean the data with forward fill
        cleaned_unrate = clean_data(unrate_data, method='forward_fill')
        print(f"\nAfter forward-fill cleaning: {len(cleaned_unrate)} rows")
        print(cleaned_unrate.head())
        
        # Save cleaned data
        save_data(cleaned_unrate, 'UNRATE', raw=False)
    else:
        print("Failed to retrieve unemployment rate data.")
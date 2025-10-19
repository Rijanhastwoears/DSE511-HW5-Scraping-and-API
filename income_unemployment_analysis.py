import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fred_client import get_series_data, save_data, clean_data
import os

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def get_income_unemployment_data(years_back=10):
    """
    Retrieve unemployment rate data for different income levels.

    Parameters:
    years_back (int): Number of years of historical data to retrieve

    Returns:
    dict: Dictionary containing DataFrames for different income unemployment series
    """
    import datetime

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * years_back)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # FRED series IDs for unemployment rates by income level
    # Note: These are the actual available series from FRED
    income_unemployment_series = {
        'LNS14000003': 'Unemployment Rate - White',
        'LNS14000006': 'Unemployment Rate - Black or African American',
        'LNS14000009': 'Unemployment Rate - Hispanic or Latino',
        'LNS14000012': 'Unemployment Rate - Asian',
        'LNS14000315': 'Unemployment Rate - Men, 20 years and over',
        'LNS14000002': 'Unemployment Rate - Women',
        'LNS14000025': 'Unemployment Rate - 16-19 years',
        'LNS14000026': 'Unemployment Rate - 20 years and over',
        'LNS14000150': 'Unemployment Rate - Married men, spouse present',
        'LNS14000327': 'Unemployment Rate - Women who maintain families'
    }

    data = {}

    for series_id, description in income_unemployment_series.items():
        print(f"Retrieving {description}...")
        df = get_series_data(series_id, start_date=start_date_str, end_date=end_date_str)
        if df is not None:
            df.columns = [description]  # Rename column to description
            data[series_id] = df
            print(f"Retrieved {len(df)} observations for {description}")
        else:
            print(f"Failed to retrieve data for {series_id}")

    return data

def create_income_trend_visualization(data_dict, save_path=None):
    """
    Create academic-style trendline visualization for income-based unemployment rates.

    Parameters:
    data_dict (dict): Dictionary of DataFrames with unemployment data
    save_path (str): Path to save the visualization (optional)
    """
    plt.figure(figsize=(16, 12))

    # Create subplots for different categories
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Unemployment Rates by Demographic Groups: 10-Year Trends',
                fontsize=16, fontweight='bold', y=0.95)

    # Define groups for subplots
    groups = {
        'Racial/Ethnic Groups': ['LNS14000003', 'LNS14000006', 'LNS14000009', 'LNS14000012'],
        'Gender Groups': ['LNS14000315', 'LNS14000002', 'LNS14000150', 'LNS14000327'],
        'Age Groups': ['LNS14000025', 'LNS14000026'],
        'All Groups': list(data_dict.keys())
    }

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    subplot_titles = ['Racial/Ethnic Groups', 'Gender Groups', 'Age Groups', 'Combined Trends']
    axes_flat = axes.flatten()

    for idx, (group_name, series_ids) in enumerate(groups.items()):
        ax = axes_flat[idx]

        for i, series_id in enumerate(series_ids):
            if series_id in data_dict and data_dict[series_id] is not None and not data_dict[series_id].empty:
                df = data_dict[series_id]
                column_name = df.columns[0]
                color = colors[i % len(colors)]

                # Plot the data
                ax.plot(df.index, df[column_name],
                       label=column_name.replace('Unemployment Rate - ', ''),
                       color=color,
                       linewidth=2,
                       alpha=0.8)

                # Add trendline using rolling mean (smoothed) - only for combined plot
                if group_name == 'All Groups' and len(df) > 12:
                    trend = df[column_name].rolling(window=12, center=True).mean()
                    ax.plot(df.index, trend,
                           color=color,
                           linestyle='--',
                           linewidth=1,
                           alpha=0.6)

        ax.set_title(subplot_titles[idx], fontsize=12, fontweight='bold')
        ax.set_xlabel('Date', fontsize=10)
        ax.set_ylabel('Unemployment Rate (%)', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
    else:
        plt.show()

def generate_income_descriptive_stats(data_dict):
    """
    Generate descriptive statistics for income-based unemployment data.

    Parameters:
    data_dict (dict): Dictionary of DataFrames with unemployment data

    Returns:
    pandas.DataFrame: Summary statistics
    """
    summary_data = []

    for series_id, df in data_dict.items():
        if df is not None and not df.empty:
            column_name = df.columns[0]
            series_data = df[column_name].dropna()

            stats = {
                'Group': column_name.replace('Unemployment Rate - ', ''),
                'Mean': series_data.mean(),
                'Median': series_data.median(),
                'Std Dev': series_data.std(),
                'Min': series_data.min(),
                'Max': series_data.max(),
                'Observations': len(series_data),
                'Latest Value': series_data.iloc[-1] if len(series_data) > 0 else None,
                '10Y Change': series_data.iloc[-1] - series_data.iloc[0] if len(series_data) > 0 else None
            }
            summary_data.append(stats)

    return pd.DataFrame(summary_data).round(2)

def create_income_summary_report(data_dict, save_dir='reports/income_analysis'):
    """
    Create a comprehensive summary report for income-based unemployment analysis.

    Parameters:
    data_dict (dict): Dictionary of DataFrames with unemployment data
    save_dir (str): Directory to save report files
    """
    os.makedirs(save_dir, exist_ok=True)

    # Generate descriptive statistics
    print("Generating descriptive statistics...")
    stats_df = generate_income_descriptive_stats(data_dict)

    # Save statistics to CSV
    stats_path = os.path.join(save_dir, 'income_unemployment_statistics.csv')
    stats_df.to_csv(stats_path, index=False)
    print(f"Statistics saved to {stats_path}")

    # Create and save visualization
    viz_path = os.path.join(save_dir, 'income_unemployment_trends.png')
    create_income_trend_visualization(data_dict, save_path=viz_path)

    # Save raw data for all series
    print("Saving raw data for all series...")
    for series_id, df in data_dict.items():
        if df is not None:
            save_data(df, f"{series_id}_income_10y", raw=True)

            # Clean and save cleaned data
            cleaned_df = clean_data(df, method='drop')
            save_data(cleaned_df, f"{series_id}_income_10y", raw=False)

    # Print summary to console
    print("\n" + "="*100)
    print("INCOME-BASED UNEMPLOYMENT RATE ANALYSIS SUMMARY")
    print("="*100)
    print(f"Analysis Period: Last 10 years")
    print(f"Number of Groups Analyzed: {len([df for df in data_dict.values() if df is not None])}")
    print(f"Raw data saved to: raw_data/")
    print(f"Cleaned data saved to: clean_data/")
    print("\nDescriptive Statistics:")
    print("-" * 80)
    print(stats_df.to_string(index=False))

    # Identify key insights
    if not stats_df.empty:
        highest_avg = stats_df.loc[stats_df['Mean'].idxmax()]
        lowest_avg = stats_df.loc[stats_df['Mean'].idxmin()]
        most_volatile = stats_df.loc[stats_df['Std Dev'].idxmax()]
        most_improved = stats_df.loc[stats_df['10Y Change'].idxmin()]  # Most negative change

        print("\nKey Insights:")
        print(f"- Highest average rate: {highest_avg['Group']} ({highest_avg['Mean']}%)")
        print(f"- Lowest average rate: {lowest_avg['Group']} ({lowest_avg['Mean']}%)")
        print(f"- Most volatile: {most_volatile['Group']} (Std Dev: {most_volatile['Std Dev']})")
        print(f"- Most improved over 10 years: {most_improved['Group']} ({most_improved['10Y Change']}%)")

    print(f"\nVisualization saved to: {viz_path}")
    print(f"Statistics saved to: {stats_path}")

if __name__ == "__main__":
    print("Starting Income-Based Unemployment Rate Analysis...")

    # Retrieve data for the last 10 years
    income_unemployment_data = get_income_unemployment_data(years_back=10)

    # Create comprehensive report
    create_income_summary_report(income_unemployment_data)

    print("\nIncome analysis complete!")
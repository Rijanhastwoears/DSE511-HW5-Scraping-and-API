import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fred_client import get_series_data, save_data, clean_data
import os

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def get_unemployment_data(years_back=10):
    """
    Retrieve unemployment rate data for different economic classes.

    Parameters:
    years_back (int): Number of years of historical data to retrieve

    Returns:
    dict: Dictionary containing DataFrames for different unemployment series
    """
    import datetime

    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365 * years_back)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # FRED series IDs for different unemployment rates
    unemployment_series = {
        'UNRATE': 'Unemployment Rate (Overall)',
        'U1RATE': 'Unemployment Rate - 15 weeks or less',
        'U2RATE': 'Unemployment Rate - Job losers',
        'U3RATE': 'Unemployment Rate - 27 weeks and over',
        'U4RATE': 'Unemployment Rate - Discouraged workers',
        'U5RATE': 'Unemployment Rate - Marginally attached',
        'U6RATE': 'Unemployment Rate - Total unemployed, plus all persons marginally attached to the labor force'
    }

    data = {}

    for series_id, description in unemployment_series.items():
        print(f"Retrieving {description}...")
        df = get_series_data(series_id, start_date=start_date_str, end_date=end_date_str)
        if df is not None:
            df.columns = [description]  # Rename column to description
            data[series_id] = df
            print(f"Retrieved {len(df)} observations for {description}")
        else:
            print(f"Failed to retrieve data for {series_id}")

    return data

def create_trend_visualization(data_dict, save_path=None):
    """
    Create academic-style trendline visualization for unemployment rates.

    Parameters:
    data_dict (dict): Dictionary of DataFrames with unemployment data
    save_path (str): Path to save the visualization (optional)
    """
    plt.figure(figsize=(15, 10))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

    for i, (series_id, df) in enumerate(data_dict.items()):
        if df is not None and not df.empty:
            column_name = df.columns[0]
            color = colors[i % len(colors)]

            # Plot the data
            plt.plot(df.index, df[column_name],
                    label=column_name,
                    color=color,
                    linewidth=2,
                    alpha=0.8)

            # Add trendline using rolling mean (smoothed)
            if len(df) > 12:  # Only add trendline if we have enough data
                trend = df[column_name].rolling(window=12, center=True).mean()
                plt.plot(df.index, trend,
                        color=color,
                        linestyle='--',
                        linewidth=1,
                        alpha=0.6,
                        label=f'{column_name} (12-month trend)')

    plt.title('Unemployment Rates by Economic Class: 10-Year Trends',
             fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Unemployment Rate (%)', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {save_path}")
    else:
        plt.show()

def generate_descriptive_stats(data_dict):
    """
    Generate descriptive statistics for unemployment data.

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
                'Series': column_name,
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

def create_summary_report(data_dict, save_dir='reports'):
    """
    Create a comprehensive summary report with statistics and visualization.

    Parameters:
    data_dict (dict): Dictionary of DataFrames with unemployment data
    save_dir (str): Directory to save report files
    """
    os.makedirs(save_dir, exist_ok=True)

    # Generate descriptive statistics
    print("Generating descriptive statistics...")
    stats_df = generate_descriptive_stats(data_dict)

    # Save statistics to CSV
    stats_path = os.path.join(save_dir, 'unemployment_statistics.csv')
    stats_df.to_csv(stats_path, index=False)
    print(f"Statistics saved to {stats_path}")

    # Create and save visualization
    viz_path = os.path.join(save_dir, 'unemployment_trends.png')
    create_trend_visualization(data_dict, save_path=viz_path)

    # Save raw data for all series
    print("Saving raw data for all series...")
    for series_id, df in data_dict.items():
        if df is not None:
            save_data(df, f"{series_id}_10y", raw=True)

    # Print summary to console
    print("\n" + "="*80)
    print("UNEMPLOYMENT RATE ANALYSIS SUMMARY")
    print("="*80)
    print(f"Analysis Period: Last 10 years")
    print(f"Number of Series Analyzed: {len([df for df in data_dict.values() if df is not None])}")
    print("\nDescriptive Statistics:")
    print("-" * 50)
    print(stats_df.to_string(index=False))

    # Identify key insights
    if not stats_df.empty:
        highest_avg = stats_df.loc[stats_df['Mean'].idxmax()]
        lowest_avg = stats_df.loc[stats_df['Mean'].idxmin()]
        most_volatile = stats_df.loc[stats_df['Std Dev'].idxmax()]

        print("\nKey Insights:")
        print(f"- Highest average rate: {highest_avg['Series']} ({highest_avg['Mean']}%)")
        print(f"- Lowest average rate: {lowest_avg['Series']} ({lowest_avg['Mean']}%)")
        print(f"- Most volatile: {most_volatile['Series']} (Std Dev: {most_volatile['Std Dev']})")

    print(f"\nVisualization saved to: {viz_path}")
    print(f"Statistics saved to: {stats_path}")

if __name__ == "__main__":
    print("Starting Unemployment Rate Analysis...")

    # Retrieve data for the last 10 years
    unemployment_data = get_unemployment_data(years_back=10)

    # Create comprehensive report
    create_summary_report(unemployment_data)

    print("\nAnalysis complete!")
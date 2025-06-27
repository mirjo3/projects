"""
Inventory Par Level Optimization System
=====================================
Analyzes historical usage data to calculate optimal inventory levels
using statistical methods including coefficient of variation analysis.

This system processes transaction data to:
- Calculate average daily usage patterns
- Determine inventory volatility using coefficient of variation
- Generate optimized minimum and maximum inventory levels
- Provide comprehensive analytics and reporting

Expected CSV Input Format:
- location_name: Storage location identifier
- item_description: Item name/description  
- item_id: Unique item identifier
- quantity: Transaction quantity
- transaction_datetime: Transaction timestamp
- transaction_type: Type of transaction (e.g., 'dispensed')
- min: Current minimum level
- max: Current maximum level

Note: This code is designed for educational/portfolio purposes.
All data should be sanitized before use in production environments.

Author: Joseph Miranda
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def get_cv_category(cv_value):
    """
    Categorize coefficient of variation into Low, Medium, or High volatility
    
    Parameters:
    cv_value (float): Coefficient of variation percentage
    
    Returns:
    str: Category classification ('Low', 'Medium', 'High')
    """
    if cv_value <= 50:
        return 'Low'
    elif cv_value <= 100:
        return 'Medium'
    else:
        return 'High'

def analyze_inventory_data(df):
    """
    Analyze inventory transaction data and calculate optimal par levels
    
    Parameters:
    df (pandas.DataFrame): Raw transaction data
    
    Returns:
    pandas.DataFrame: Processed data with suggested par levels and analytics
    """
    try:
        print("\nStarting data analysis...")
        print(f"Initial data shape: {df.shape}")
        
        # Standardize column names and data formatting
        df.columns = df.columns.str.lower()
        df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)
        
        # Rename columns for consistency
        df = df.rename(columns={
            'stationname': 'location_name',
            'meddescription': 'item_description',
            'medid': 'item_id',
            'transactiondatetime': 'transaction_datetime',
            'transactiontype': 'transaction_type'
        })
        
        # Convert numeric columns, handling any non-numeric values
        numeric_columns = ['quantity', 'min', 'max']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convert and handle datetime
        df['transaction_datetime'] = pd.to_datetime(df['transaction_datetime'])
        df['date'] = df['transaction_datetime'].dt.date
        
        # Calculate analysis period information
        start_date = df['transaction_datetime'].min()
        end_date = df['transaction_datetime'].max()
        total_days = (end_date - start_date).days + 1
        
        print(f"\nAnalysis Period:")
        print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"End Date: {end_date.strftime('%Y-%m-%d')}")
        print(f"Total Days in Period: {total_days}")
        
        print(f"\nUnique transaction types found: {df['transaction_type'].unique()}")
        
        # Filter for dispensed transactions only (usage/consumption events)
        usage_df = df[df['transaction_type'].isin(['vend', 'dispensed', 'usage'])].copy()
        print(f"Number of usage transactions: {len(usage_df)}")
        
        # Group by location, item, and date to calculate daily usage
        daily_usage = usage_df.groupby(['location_name', 'item_description', 'item_id', 'date'])['quantity'].sum().reset_index()
        print(f"Number of unique daily usage records: {len(daily_usage)}")
        
        # Calculate comprehensive metrics for each location-item combination
        location_item_metrics = []
        
        for (location, item, item_id), group in daily_usage.groupby(['location_name', 'item_description', 'item_id']):
            # Calculate total usage and usage patterns
            total_usage = group['quantity'].sum()
            days_with_usage = len(group)
            usage_frequency = round((days_with_usage / total_days * 100), 2)
            
            # Calculate average daily use based on usage frequency
            # High turnover items: calculate based on total period
            # Low turnover items: calculate based on active usage days
            if usage_frequency >= 75:  # High turnover items
                average_daily_use = round(total_usage / total_days, 2)
            else:  # Low turnover items
                average_daily_use = round(total_usage / days_with_usage, 2) if days_with_usage > 0 else 0
            
            # Calculate variability metrics
            max_used = group['quantity'].max()
            std_dev = round(group['quantity'].std(ddof=0) if len(group) > 1 else 0, 2)
            
            location_item_metrics.append({
                'location_name': location,
                'item_description': item,
                'item_id': item_id,
                'average_daily_use': average_daily_use,
                'max_used': max_used,
                'standard_deviation': std_dev,
                'days_with_usage': days_with_usage,
                'total_days': total_days,
                'usage_frequency': usage_frequency
            })
        
        # Convert to DataFrame for analysis
        metrics = pd.DataFrame(location_item_metrics)
        
        # Calculate coefficient of variation (CV) - key volatility metric
        metrics['coefficient_of_variation'] = np.where(
            metrics['average_daily_use'] != 0,
            (metrics['standard_deviation'] / metrics['average_daily_use'] * 100).round(2),
            0
        )
        
        # Categorize items by volatility
        metrics['cv_category'] = metrics['coefficient_of_variation'].apply(get_cv_category)
        
        # Merge current par levels from original data
        current_pars = usage_df.groupby(['location_name', 'item_description', 'item_id'])[['min', 'max']].first()
        metrics = metrics.merge(current_pars, on=['location_name', 'item_description', 'item_id'])
        
        # Calculate optimized par levels based on volatility category
        # High Volatility (CV > 100%): Conservative approach using max usage
        # Medium Volatility (50% < CV <= 100%): Statistical safety stock method
        # Low Volatility (CV <= 50%): Simple multiplication method
        
        metrics['suggested_min'] = np.where(
            metrics['coefficient_of_variation'] > 100,
            # High volatility: 3-day supply based on maximum observed usage
            (metrics['max_used'] * 3).round(0),
            np.where(
                (metrics['coefficient_of_variation'] > 50) & (metrics['coefficient_of_variation'] <= 100),
                # Medium volatility: Average daily use * lead time + statistical safety stock
                ((metrics['average_daily_use'] * 3) + 
                 (1.96 * metrics['standard_deviation'] * np.sqrt(3))).round(0),
                # Low volatility: Simple average daily use * lead time
                (metrics['average_daily_use'] * 3).round(0)
            )
        )
        
        # Calculate suggested maximum levels
        metrics['suggested_max'] = np.where(
            metrics['coefficient_of_variation'] > 100,
            # High volatility: 10-day supply based on maximum usage
            (metrics['max_used'] * 10).round(0),
            np.where(
                (metrics['coefficient_of_variation'] > 50) & (metrics['coefficient_of_variation'] <= 100),
                # Medium volatility: 10-day supply + safety stock
                ((metrics['average_daily_use'] * 10) + 
                 (1.96 * metrics['standard_deviation'] * np.sqrt(10))).round(0),
                # Low volatility: Simple 10-day supply
                (metrics['average_daily_use'] * 10).round(0)
            )
        )
        
        # Apply business rules and constraints
        metrics['suggested_min'] = metrics['suggested_min'].clip(lower=1)  # Minimum of 1 unit
        metrics['suggested_max'] = np.maximum(metrics['suggested_max'], metrics['suggested_min'])  # Max >= Min
        
        # Organize output columns for reporting
        final_columns = [
            'location_name', 
            'item_description', 
            'item_id',
            'suggested_min',
            'suggested_max',
            'cv_category',
            'usage_frequency',
            'average_daily_use',
            'max_used',
            'min', 
            'max',
            'standard_deviation', 
            'days_with_usage',
            'total_days',
            'coefficient_of_variation', 
        ]
        
        print("\nAnalysis completed successfully!")
        return metrics[final_columns]
        
    except Exception as e:
        print(f"Error in analyze_inventory_data: {str(e)}")
        raise

def main():
    """
    Main execution function for inventory par level optimization
    """
    try:
        print("=" * 60)
        print("Inventory Par Level Optimization System")
        print("=" * 60)
        
        # Get input file from user
        input_path = input("\nPlease enter the full path to your CSV file: ")
        
        # Validate input file
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"The file does not exist: {input_path}")
        
        if not input_path.lower().endswith('.csv'):
            raise ValueError("The file must be a CSV file")
        
        # Determine output directory
        output_dir = os.path.dirname(input_path)
        if not output_dir:
            output_dir = '.'
            
        print("\nReading CSV file...")
        
        # Read and validate CSV file
        df = pd.read_csv(input_path, low_memory=False)
        
        if df.empty:
            raise ValueError("The CSV file is empty")
            
        print(f"Successfully read CSV file with {len(df)} rows")
        
        # Process the inventory data
        results = analyze_inventory_data(df)
        
        # Generate timestamped output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_filename = f"optimized_par_levels_{timestamp}.csv"
        output_path = os.path.join(output_dir, output_filename)
        
        # Save results to CSV
        results.to_csv(output_path, index=False)
        print(f"\nResults saved to: {output_path}")
        
        # Generate comprehensive summary report
        print("\n" + "=" * 60)
        print("ANALYSIS SUMMARY REPORT")
        print("=" * 60)
        
        print(f"Total locations analyzed: {len(results['location_name'].unique())}")
        print(f"Total items analyzed: {len(results['item_description'].unique())}")
        print(f"Total location-item combinations: {len(results)}")
        
        # Volatility analysis
        print("\nVolatility Analysis (Coefficient of Variation):")
        cv_counts = results['cv_category'].value_counts()
        for category, count in cv_counts.items():
            percentage = (count / len(results) * 100)
            print(f"  {category} volatility items: {count} ({percentage:.1f}%)")
        
        # Usage frequency analysis
        print("\nUsage Frequency Distribution:")
        freq_ranges = [(0, 25, "Rarely used"), (25, 50, "Occasionally used"), 
                      (50, 75, "Frequently used"), (75, 100, "Daily use")]
        for low, high, description in freq_ranges:
            count = len(results[(results['usage_frequency'] >= low) & (results['usage_frequency'] < high)])
            percentage = (count / len(results) * 100)
            print(f"  {description} ({low}-{high}% of days): {count} ({percentage:.1f}%)")
        
        # Par level adjustment analysis
        print("\nPar Level Optimization Results:")
        
        # Convert to numeric for comparison
        results['min'] = pd.to_numeric(results['min'], errors='coerce')
        results['max'] = pd.to_numeric(results['max'], errors='coerce')
        
        # Minimum level changes
        increased_min = len(results[results['suggested_min'] > results['min']])
        decreased_min = len(results[results['suggested_min'] < results['min']])
        unchanged_min = len(results[results['suggested_min'] == results['min']])
        
        print(f"  Minimum levels - Increase recommended: {increased_min}")
        print(f"  Minimum levels - Decrease recommended: {decreased_min}")
        print(f"  Minimum levels - No change needed: {unchanged_min}")
        
        # Maximum level changes
        increased_max = len(results[results['suggested_max'] > results['max']])
        decreased_max = len(results[results['suggested_max'] < results['max']])
        unchanged_max = len(results[results['suggested_max'] == results['max']])
        
        print(f"  Maximum levels - Increase recommended: {increased_max}")
        print(f"  Maximum levels - Decrease recommended: {decreased_max}")
        print(f"  Maximum levels - No change needed: {unchanged_max}")
        
        print("\n" + "=" * 60)
        print("Analysis completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
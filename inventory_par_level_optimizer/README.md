# Inventory Par Level Optimization System

A Python-based analytics tool that calculates optimal inventory levels using statistical analysis and volatility assessment. This system processes historical transaction data to generate data-driven par level recommendations that balance inventory with service level requirements.

## Project Overview

This project analyzes inventory usage patterns across multiple locations to optimize minimum and maximum stock levels. By leveraging statistical methods including standard deviation and coefficient of variation, the system categorizes items by volatility and applies appropriate inventory management strategies.

**Key Features:**
- Flexible time period analysis (quarterly, yearly, custom ranges)
- Advanced statistical volatility assessment
- Risk-based inventory categorization
- Automated par level calculation with safety stock
- Comprehensive reporting and analytics

## Methodology

### Data Processing Pipeline

1. **Data Extraction & Cleaning**
   - Processes transaction data from any specified time period
   - Standardizes column formats and handles missing values
   - Filters for relevant transaction types (dispensed, returns, usage)

2. **Usage Pattern Analysis**
   - Calculates daily usage rates across all locations and items
   - Analyzes dispensing frequency and return patterns
   - Determines usage consistency over the analysis period

3. **Statistical Volatility Assessment**
   - **Standard Deviation**: Measures absolute variability in daily usage
   - **Coefficient of Variation (CV)**: Measures relative variability (σ/μ × 100)
   - **Usage Frequency**: Percentage of days with recorded transactions

### Volatility-Based Categorization

Items are classified into three volatility categories based on their coefficient of variation:

| Category | CV Range | Characteristics | Strategy |
|----------|----------|----------------|----------|
| **Low** | ≤ 50% | Predictable, consistent usage | Standard safety stock |
| **Medium** | 51-100% | Moderate variability | Statistical safety stock |
| **High** | > 100% | Highly unpredictable usage | Conservative max-based approach |

### Par Level Calculation Strategy

The system employs a **3-day minimum, 10-day maximum** baseline with volatility-adjusted calculations:

#### Minimum Par Level Calculation

**Low Volatility (CV ≤ 50%):**
```
Min = Average Daily Use × 3 days
```

**Medium Volatility (50% < CV ≤ 100%):**
```
Min = (Average Daily Use × 3) + (1.96 × Standard Deviation × √3)
```
*Uses statistical safety stock with 95% confidence interval*

**High Volatility (CV > 100%):**
```
Min = Maximum Daily Use × 3 days
```
*Conservative approach based on peak usage patterns*

#### Maximum Par Level Calculation

**Low Volatility:**
```
Max = Average Daily Use × 10 days
```

**Medium Volatility:**
```
Max = (Average Daily Use × 10) + (1.96 × Standard Deviation × √10)
```

**High Volatility:**
```
Max = Maximum Daily Use × 10 days
```

### Statistical Foundation

The methodology incorporates several key statistical concepts:

- **Safety Stock Formula**: `1.96 × σ × √L` where σ is standard deviation and L is lead time
- **Service Level**: 95% confidence interval (Z-score = 1.96)
- **Lead Time Consideration**: 3-day replenishment assumption for minimums
- **Review Period**: 10-day maximum capacity planning

## Getting Started

### Prerequisites

```bash
pip install pandas numpy
```

### Input Data Format

The system expects CSV files with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `location_name` | Storage location identifier | "Unit-A", "Floor-2" |
| `item_description` | Item name/description | "Antibiotic-1", "Supply-X" |
| `item_id` | Unique item identifier | "MED001", "SUP123" |
| `quantity` | Transaction quantity | 5, -2 (returns) |
| `transaction_datetime` | Transaction timestamp | "2024-01-15 14:30:00" |
| `transaction_type` | Transaction type | "dispensed", "returned" |
| `min` | Current minimum level | 10 |
| `max` | Current maximum level | 50 |

### Usage

1. **Run the analyzer:**
   ```bash
   python inventory_par_level_optimizer.py
   ```

2. **Enter your data file path when prompted**

3. **Review the generated output file:**
   - Filename format: `optimized_par_levels_YYYYMMDD_HHMM.csv`

## Sample Results

### Analysis Summary Output

```
ANALYSIS SUMMARY REPORT
======================
Total locations analyzed: 15
Total items analyzed: 234
Total location-item combinations: 445

Volatility Analysis:
  Low volatility items: 267 (60.0%)
  Medium volatility items: 134 (30.1%)
  High volatility items: 44 (9.9%)

Par Level Optimization Results:
  Minimum levels - Increase recommended: 156
  Minimum levels - Decrease recommended: 89
  Maximum levels - Increase recommended: 201
```

### Output File Columns

| Column | Description |
|--------|-------------|
| `suggested_min` | Optimized minimum par level |
| `suggested_max` | Optimized maximum par level |
| `cv_category` | Volatility classification |
| `usage_frequency` | Percentage of days with usage |
| `average_daily_use` | Mean daily consumption |
| `coefficient_of_variation` | Volatility percentage |

## Business Impact

**Cost Optimization:**
- Reduces excess inventory through data-driven max levels
- Prevents stockouts with statistically-calculated safety stock
- Balances carrying costs with service level requirements

**Risk Management:**
- Identifies high-volatility items requiring special attention
- Provides confidence intervals for inventory planning
- Adapts par levels to actual usage patterns

**Operational Efficiency:**
- Automates manual par level review processes
- Standardizes inventory management across locations
- Provides actionable insights for procurement decisions

## Technical Implementation

**Core Technologies:**
- **Python**: Primary development language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Statistical calculations
- **Statistical Methods**: CV analysis, safety stock calculation

**Key Algorithms:**
- Coefficient of variation-based volatility assessment
- Statistical safety stock with normal distribution assumptions
- Dynamic par level adjustment based on usage patterns
- Time series analysis for trend identification

## File Structure

```
inventory-optimizer/
│
├── inventory_par_level_optimizer.py    # Main analysis script
├── README.md                           # This documentation
├── requirements.txt                    # Python dependencies
└── sample_data/                        # Example datasets (sanitized)
    └── sample_transactions.csv
```

## Future Enhancements

- **Seasonal Adjustment**: Incorporate seasonal usage patterns
- **Lead Time Optimization**: Dynamic lead time calculation
- **Cost Analysis**: Integration with item cost data
- **Forecasting**: Predictive analytics for future demand
- **Dashboard**: Interactive visualization interface

## Portfolio Highlights

This project demonstrates:
- **Advanced Statistical Analysis**: CV, standard deviation, confidence intervals
- **Business Process Optimization**: Inventory management methodology
- **Data Engineering**: Robust data processing and validation
- **Risk Assessment**: Volatility-based categorization strategies
- **Scalable Solutions**: Handles multiple locations and item types

---

*Note: This project was developed for educational and portfolio demonstration purposes. All sample data has been sanitized to protect confidential information.*

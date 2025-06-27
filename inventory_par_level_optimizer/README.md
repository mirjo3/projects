# Inventory Par Level Optimization System

Python tool that calculates optimal inventory levels using statistical analysis. Processes transaction data to recommend minimum and maximum stock levels that balance costs with service requirements.

## Overview

Analyzes inventory usage patterns across multiple locations to optimize stock levels. Uses coefficient of variation and standard deviation to categorize items by volatility and calculate appropriate inventory levels.

**Key Features:**
- Statistical volatility assessment 
- Risk-based inventory categorization
- Automated par level calculation with safety stock
- Multi-location analysis support

## How It Works

### 1. Data Processing
- Extracts transaction data from CSV files
- Calculates daily usage rates by location and item
- Analyzes usage consistency over time

### 2. Volatility Classification
Items categorized by coefficient of variation (CV):

| Category | CV Range | Strategy |
|----------|----------|----------|
| **Low** | ≤ 50% | Standard 3-day minimum |
| **Medium** | 51-100% | Statistical safety stock |
| **High** | > 100% | Conservative max-based approach |

### 3. Par Level Calculation

**Minimum Levels:**
- Low volatility: `Average Daily Use × 3`
- Medium volatility: `(Average Daily Use × 3) + Statistical Safety Stock`
- High volatility: `Maximum Daily Use × 3`

**Maximum Levels:** Same logic with 10-day multiplier

## Usage

```bash
pip install pandas numpy
python inventory_par_level_optimizer.py
```

**Input:** CSV with columns: `location_name`, `item_description`, `quantity`, `transaction_datetime`, `transaction_type`

**Output:** Optimized par levels with volatility analysis

## Sample Results

```
Total items analyzed: 445
Volatility breakdown:
  Low: 267 (60%)
  Medium: 134 (30%) 
  High: 44 (10%)

Recommendations:
  Increase minimums: 156 items
  Decrease minimums: 89 items
```

## Business Impact

- **Cost Reduction:** Eliminates excess inventory through data-driven maximums
- **Risk Management:** Prevents stockouts with statistical safety stock
- **Automation:** Replaces manual par level reviews

## Technologies

- **Python:** Pandas, NumPy
- **Statistics:** Coefficient of variation, safety stock formulas
- **Methods:** Time series analysis, volatility assessment

## File Structure

```
inventory-optimizer/
├── inventory_par_level_optimizer.py    # Main analysis script
├── README.md                           # Documentation
├── requirements.txt                    # Dependencies
└── sample_data/
    └── sample_transactions.csv
```

**Key Algorithms:**
- Coefficient of variation-based volatility assessment
- Statistical safety stock with normal distribution assumptions
- Dynamic par level adjustment based on usage patterns
- Time series analysis for trend identification

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

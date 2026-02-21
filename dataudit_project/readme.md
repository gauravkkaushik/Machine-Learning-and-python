# dataudit

`dataudit` is a Python package for automated data profiling and Excel-based audit reporting.
It accepts a dataset, profiles numerical and categorical features, computes correlations, and produces a multi-sheet report including a final `Red Flags` sheet for quick issue triage.

## Table of Contents

1. Overview
2. Project Structure
3. Installation
4. Input Support
5. Usage
6. Report Sheets
7. Red Flag Rules
8. Public API
9. Error Handling
10. Troubleshooting

## Overview

`dataudit` is designed for:

- exploratory data quality checks
- pre-modeling data validation
- quick feature-level risk detection
- generating shareable profiling output for business and engineering stakeholders

Core capabilities:

- accepts `pandas.DataFrame` or file path input
- profiles numerical columns with distribution, sparsity, and outlier statistics
- profiles categorical columns with nulls, cardinality, and top-frequency values
- builds Pearson correlation matrix for numeric columns
- writes a clean, multi-sheet Excel report using `openpyxl`
- includes a dedicated `Red Flags` sheet as the last tab

## Project Structure

```text
dataudit_project/
|-- setup.py
|-- readme.md
`-- dataudit/
    |-- __init__.py
    `-- core.py
```

## Installation

Run from inside `dataudit_project`:

```bash
pip install -e .
```

Dependencies are managed in `setup.py`:

- `numpy>=1.23,<2`
- `pandas>=1.5`
- `openpyxl>=3.1`

## Input Support

You can initialize `Profiler` with:

- a `pandas.DataFrame`
- a CSV file path (`.csv`)
- an Excel file path (`.xlsx`, `.xls`, `.xlsm`, `.xlsb`)
- a Parquet file path (`.parquet`)

Example:

```python
from dataudit import Profiler

profiler = Profiler("customer_data.csv")
```

Unsupported formats raise a clear `ValueError`.
Missing files raise `FileNotFoundError`.

## Usage

### Minimal Example

```python
import pandas as pd
from dataudit import Profiler

df = pd.read_csv("sample.csv")
profiler = Profiler(df)

overview_df = profiler.get_overview()
num_df = profiler.profile_numerical()
cat_df = profiler.profile_categorical()
flags_df = profiler.profile_red_flags()

output_path = profiler.export_report("Data_Audit_Report.xlsx")
print(output_path)
```

### File Path Example

```python
from dataudit import Profiler

profiler = Profiler("transactions.parquet")
profiler.export_report("Transactions_Audit.xlsx")
```

## Report Sheets

`export_report()` generates the following sheets in order:

1. `Executive Summary`
2. `Numerical Profile`
3. `Categorical Profile`
4. `Correlations`
5. `Red Flags` (last sheet)

### 1) Executive Summary

Contains:

- Total Rows
- Total Columns
- Duplicate Rows (count and percent)
- Memory Usage (MB)
- Data type breakdown

### 2) Numerical Profile

For each numeric feature:

- 5-point summary: Min, Q1, Median, Q3, Max
- Mean, Std Dev
- Skewness, Kurtosis
- Zeros (count and percent)
- Nulls (count and percent)
- Unique values
- Outliers (1.5 * IQR rule)
- 3 sample non-null values

### 3) Categorical Profile

For each categorical/object feature:

- Nulls (count and percent)
- Unique values
- Top 1 to Top 5 values with percentages
- High Cardinality Flag (`True` when unique values > 50)

### 4) Correlations

- Pearson correlation matrix for numerical columns
- If no numerical columns exist, an info message is written instead

### 5) Red Flags

Columns:

- `Feature`
- `Comments`

This sheet is intentionally concise for quick risk review.

## Red Flag Rules

`profile_red_flags()` and the `Red Flags` sheet currently detect:

- `Outliers`: numeric values outside `Q1 - 1.5*IQR` and `Q3 + 1.5*IQR`
- `High Cardinality`: categorical features with more than 50 unique non-null values
- `Single-Value Feature`: features with exactly 1 unique non-null value
- `All Null Feature`: features with 0 unique non-null values (all missing)

If a feature matches multiple rules, comments are merged in one row.

## Public API

- `Profiler(data)`
- `Profiler.get_overview() -> pandas.DataFrame`
- `Profiler.profile_numerical() -> pandas.DataFrame`
- `Profiler.profile_categorical() -> pandas.DataFrame`
- `Profiler.profile_red_flags() -> pandas.DataFrame`
- `Profiler.export_report(output_filename="Data_Audit_Report.xlsx") -> str`

## Error Handling

Built-in safeguards include:

- safe percentage calculations for empty datasets (no division-by-zero)
- fallback report messages when numerical/categorical columns are absent
- graceful handling of empty DataFrames
- explicit file-format and file-existence checks
- helpful Parquet dependency message if parquet engine is unavailable

## Troubleshooting

### NumPy ABI Import Error

If you see an error similar to:

`A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x`

Repair your environment with:

```bash
pip uninstall -y numpy pandas
pip install --no-cache-dir --force-reinstall "numpy<2" "pandas>=1.5" "openpyxl>=3.1"
pip install -e .
```

For conda environments:

```bash
conda install -y "numpy<2" pandas openpyxl
pip install -e . --no-deps
```

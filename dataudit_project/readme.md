# dataudit

`dataudit` is a Python package for end-to-end dataset profiling and Excel report generation.

## Features

- Accepts input as:
  - `pandas.DataFrame`
  - CSV file path
  - Excel file path (`.xlsx`, `.xls`, `.xlsm`, `.xlsb`)
  - Parquet file path
- Builds:
  - Executive summary
  - Numerical profiling table
  - Categorical profiling table
  - Numerical correlation matrix
- Exports all outputs into a multi-sheet Excel report.

## Project Structure

```text
dataudit_project/
├── setup.py
└── dataudit/
    ├── __init__.py
    └── core.py
```

## Installation

From inside `dataudit_project`:

```bash
pip install -e .
```

Dependencies:

- pandas
- numpy
- openpyxl

Note: `dataudit` currently pins `numpy<2` to avoid ABI incompatibility with packages compiled against NumPy 1.x.

## Quick Start

```python
import pandas as pd
from dataudit import Profiler

# Option 1: DataFrame input
df = pd.read_csv("your_data.csv")
profiler = Profiler(df)

# Option 2: File path input
# profiler = Profiler("your_data.csv")
# profiler = Profiler("your_data.xlsx")
# profiler = Profiler("your_data.parquet")

overview = profiler.get_overview()
num_profile = profiler.profile_numerical()
cat_profile = profiler.profile_categorical()

report_path = profiler.export_report("Data_Audit_Report.xlsx")
print("Report created:", report_path)
```

## Report Sheets

`export_report()` creates:

1. `Executive Summary`
2. `Numerical Profile`
3. `Categorical Profile`
4. `Correlations`

The implementation gracefully handles empty datasets and missing numerical/categorical columns.

## API

- `Profiler(data)`
- `Profiler.get_overview() -> pandas.DataFrame`
- `Profiler.profile_numerical() -> pandas.DataFrame`
- `Profiler.profile_categorical() -> pandas.DataFrame`
- `Profiler.export_report(output_filename="Data_Audit_Report.xlsx") -> str`

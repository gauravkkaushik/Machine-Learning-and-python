"""Core profiling engine for the dataudit package."""

from pathlib import Path
from typing import Any, List, Union

import numpy as np
import pandas as pd


DataInput = Union[pd.DataFrame, str, Path]


class Profiler:
    """Generate data profiling summaries and multi-sheet Excel audit reports."""

    def __init__(self, data: DataInput) -> None:
        """
        Initialize the profiler with a DataFrame or a supported file path.

        Supported input path formats: CSV, Excel, Parquet.
        """
        self.df: pd.DataFrame = self._load_data(data)
        self.num_cols: List[str] = self.df.select_dtypes(include=[np.number]).columns.tolist()
        self.cat_cols: List[str] = self.df.select_dtypes(
            include=["object", "category", "bool"]
        ).columns.tolist()

    @staticmethod
    def _load_data(data: DataInput) -> pd.DataFrame:
        """Load data from a DataFrame or supported file type."""
        if isinstance(data, pd.DataFrame):
            return data.copy()

        if isinstance(data, (str, Path)):
            file_path = Path(data)
            if not file_path.exists():
                raise FileNotFoundError("Input file not found: {0}".format(file_path))

            suffix = file_path.suffix.lower()
            if suffix == ".csv":
                return pd.read_csv(file_path)
            if suffix in {".xlsx", ".xls", ".xlsm", ".xlsb"}:
                return pd.read_excel(file_path)
            if suffix == ".parquet":
                try:
                    return pd.read_parquet(file_path)
                except ImportError as exc:
                    raise ImportError(
                        "Reading Parquet requires 'pyarrow' or 'fastparquet' to be installed."
                    ) from exc

            raise ValueError(
                "Unsupported file format. Use a pandas DataFrame or a path to CSV, Excel, or Parquet."
            )

        raise TypeError(
            "Invalid input type. 'data' must be a pandas DataFrame or a file path string."
        )

    @staticmethod
    def _safe_percentage(part: Union[int, float], whole: Union[int, float]) -> float:
        """Return a safe percentage value and avoid division-by-zero."""
        if whole == 0:
            return 0.0
        return (float(part) / float(whole)) * 100.0

    @staticmethod
    def _format_top_value(value: Any, percentage: float) -> str:
        """Format a top-category value as 'value (xx.x%)'."""
        pct = "{0:.2f}".format(percentage).rstrip("0").rstrip(".")
        return "{0} ({1}%)".format(value, pct)

    def get_overview(self) -> pd.DataFrame:
        """
        Build executive dataset-level summary metrics.

        Returns:
            DataFrame with row/column count, duplicates, memory usage, and dtype breakdown.
        """
        total_rows = int(self.df.shape[0])
        total_cols = int(self.df.shape[1])
        duplicate_rows = int(self.df.duplicated().sum()) if total_rows > 0 else 0
        duplicate_pct = self._safe_percentage(duplicate_rows, total_rows)
        memory_mb = float(self.df.memory_usage(deep=True).sum()) / (1024 * 1024)

        rows = [
            {"Metric": "Total Rows", "Value": total_rows},
            {"Metric": "Total Columns", "Value": total_cols},
            {"Metric": "Duplicate Rows (Count)", "Value": duplicate_rows},
            {"Metric": "Duplicate Rows (%)", "Value": round(duplicate_pct, 2)},
            {"Metric": "Memory Usage (MB)", "Value": round(memory_mb, 4)},
        ]

        dtype_counts = self.df.dtypes.astype(str).value_counts()
        for dtype_name, count in dtype_counts.items():
            rows.append({"Metric": "Data Type: {0}".format(dtype_name), "Value": int(count)})

        return pd.DataFrame(rows)

    def profile_numerical(self) -> pd.DataFrame:
        """
        Profile all numerical columns.

        Returns:
            DataFrame with distribution, quality, and outlier metrics per numeric feature.
        """
        columns = [
            "Feature",
            "Min",
            "Q1 (25%)",
            "Median",
            "Q3 (75%)",
            "Max",
            "Mean",
            "Std Dev",
            "Skewness",
            "Kurtosis",
            "Zeros",
            "Zeros (%)",
            "Nulls",
            "Nulls (%)",
            "Unique Values",
            "Outliers (1.5*IQR)",
            "Sample 1",
            "Sample 2",
            "Sample 3",
        ]

        if not self.num_cols:
            return pd.DataFrame(columns=columns)

        profiled_rows = []
        for col in self.num_cols:
            series = self.df[col]
            non_null = series.dropna()
            total_count = int(series.shape[0])

            null_count = int(series.isna().sum())
            null_pct = self._safe_percentage(null_count, total_count)

            zero_count = int((series == 0).sum())
            zero_pct = self._safe_percentage(zero_count, total_count)

            unique_count = int(series.nunique(dropna=True))

            if non_null.empty:
                min_val = np.nan
                q1 = np.nan
                median = np.nan
                q3 = np.nan
                max_val = np.nan
                mean_val = np.nan
                std_val = np.nan
                skew_val = np.nan
                kurt_val = np.nan
                outlier_count = 0
                samples: List[Any] = []
            else:
                min_val = non_null.min()
                q1 = non_null.quantile(0.25)
                median = non_null.quantile(0.5)
                q3 = non_null.quantile(0.75)
                max_val = non_null.max()
                mean_val = non_null.mean()
                std_val = non_null.std()
                skew_val = non_null.skew()
                kurt_val = non_null.kurtosis()

                iqr = q3 - q1
                lower_bound = q1 - (1.5 * iqr)
                upper_bound = q3 + (1.5 * iqr)
                outlier_count = int(((non_null < lower_bound) | (non_null > upper_bound)).sum())
                samples = non_null.head(3).tolist()

            while len(samples) < 3:
                samples.append(None)

            profiled_rows.append(
                {
                    "Feature": col,
                    "Min": min_val,
                    "Q1 (25%)": q1,
                    "Median": median,
                    "Q3 (75%)": q3,
                    "Max": max_val,
                    "Mean": mean_val,
                    "Std Dev": std_val,
                    "Skewness": skew_val,
                    "Kurtosis": kurt_val,
                    "Zeros": zero_count,
                    "Zeros (%)": round(zero_pct, 2),
                    "Nulls": null_count,
                    "Nulls (%)": round(null_pct, 2),
                    "Unique Values": unique_count,
                    "Outliers (1.5*IQR)": outlier_count,
                    "Sample 1": samples[0],
                    "Sample 2": samples[1],
                    "Sample 3": samples[2],
                }
            )

        return pd.DataFrame(profiled_rows, columns=columns)

    def profile_categorical(self) -> pd.DataFrame:
        """
        Profile all categorical/object columns.

        Returns:
            DataFrame with nulls, cardinality, top categories, and high-cardinality flag.
        """
        columns = [
            "Feature",
            "Nulls",
            "Nulls (%)",
            "Unique Values",
            "Top 1",
            "Top 2",
            "Top 3",
            "Top 4",
            "Top 5",
            "High Cardinality Flag",
        ]

        if not self.cat_cols:
            return pd.DataFrame(columns=columns)

        profiled_rows = []
        for col in self.cat_cols:
            series = self.df[col]
            total_count = int(series.shape[0])

            null_count = int(series.isna().sum())
            null_pct = self._safe_percentage(null_count, total_count)

            unique_count = int(series.nunique(dropna=True))
            high_cardinality = unique_count > 50

            value_counts = series.value_counts(dropna=True)
            top_values: List[str] = []
            for value, count in value_counts.head(5).items():
                pct = self._safe_percentage(int(count), total_count)
                top_values.append(self._format_top_value(value, pct))

            while len(top_values) < 5:
                top_values.append(None)

            profiled_rows.append(
                {
                    "Feature": col,
                    "Nulls": null_count,
                    "Nulls (%)": round(null_pct, 2),
                    "Unique Values": unique_count,
                    "Top 1": top_values[0],
                    "Top 2": top_values[1],
                    "Top 3": top_values[2],
                    "Top 4": top_values[3],
                    "Top 5": top_values[4],
                    "High Cardinality Flag": high_cardinality,
                }
            )

        return pd.DataFrame(profiled_rows, columns=columns)

    def export_report(self, output_filename: str = "Data_Audit_Report.xlsx") -> str:
        """
        Export a multi-sheet Excel data audit report.

        Sheets:
            1) Executive Summary
            2) Numerical Profile
            3) Categorical Profile
            4) Correlations
        """
        overview_df = self.get_overview()
        numerical_df = self.profile_numerical()
        categorical_df = self.profile_categorical()

        if self.num_cols:
            correlation_df = self.df[self.num_cols].corr(method="pearson")
        else:
            correlation_df = pd.DataFrame(
                {"Info": ["No numerical columns available for correlation analysis."]}
            )

        if numerical_df.empty:
            numerical_df = pd.DataFrame({"Info": ["No numerical columns available to profile."]})

        if categorical_df.empty:
            categorical_df = pd.DataFrame({"Info": ["No categorical columns available to profile."]})

        with pd.ExcelWriter(output_filename, engine="openpyxl") as writer:
            overview_df.to_excel(writer, sheet_name="Executive Summary", index=False)
            numerical_df.to_excel(writer, sheet_name="Numerical Profile", index=False)
            categorical_df.to_excel(writer, sheet_name="Categorical Profile", index=False)

            corr_index = "Info" not in correlation_df.columns
            correlation_df.to_excel(writer, sheet_name="Correlations", index=corr_index)

        return output_filename

from datetime import datetime
import os
from pathlib import Path

from datacompy import Compare
import pandas as pd
from pandas_profiling import ProfileReport

FIRST_CSV = "FIRST_CSV"
SECOND_CSV = "SECOND_CSV"
CSV = "CSV"


class ReportGenerator:

    _BTN_DATACOMPY_REPORT = "Datacompy"
    _BTN_PANDAS_PROFILING_REPORT = "Pandas Profiling"

    def __init__(self):

        self._report_func_dict = {
            self._BTN_DATACOMPY_REPORT: self._generate_datacompy_report,
            self._BTN_PANDAS_PROFILING_REPORT: self._generate_pandas_profiling_report,
        }

    def generate_reports(self, **report_data):

        timestamp = str(datetime.now().timestamp())

        self._data_dir = Path(f"Reports_{timestamp}")

        self._data_dir.mkdir()

        for report_type, report_option_list in report_data.items():

            for report_options in report_option_list:

                self._report_func_dict[report_type](**report_options)

        return self._data_dir

    def _generate_datacompy_report(self, **kwargs):

        df1_name, df2_name = [Path(df).stem for df in kwargs["dfs"]]

        df1, df2 = [pd.read_feather(df) for df in kwargs["dfs"]]

        join_columns = kwargs["join_columns"]

        comparison = Compare(
            df1, df2, join_columns=join_columns, df1_name=df1_name, df2_name=df2_name,
        )

        report_name_data_dict = {
            self._data_dir.joinpath("Intersection.csv"): comparison.intersect_rows,
            self._data_dir.joinpath("Only In First.csv"): comparison.df1_unq_rows,
            self._data_dir.joinpath("Only In Second.csv"): comparison.df2_unq_rows,
        }

        for name, df in report_name_data_dict.items():

            df.to_csv(name)

        with open(self._data_dir.joinpath("Report.txt"), "w+") as out_file:

            out_file.write(comparison.report())

    def _generate_pandas_profiling_report(self, **kwargs):

        df = kwargs["df"]

        report_title = Path(df).stem + ".html"

        df = pd.read_feather(df)

        report = ProfileReport(df, title=report_title)

        report.to_file(self._data_dir.joinpath(report_title))

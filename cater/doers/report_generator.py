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
    def generate_datacompy_report(self, **kwargs):

        first_csv = kwargs[FIRST_CSV]

        second_csv = kwargs[SECOND_CSV]

        df1, df1_name = self._get_df_and_name_from_csv(first_csv)

        df2, df2_name = self._get_df_and_name_from_csv(second_csv)

        # TODO The user should get a say in this.
        join_columns = df1.columns

        comparison = Compare(
            df1, df2, join_columns=join_columns, df1_name=df1_name, df2_name=df2_name
        )

        timestamp = str(datetime.now().timestamp())

        data_dir = f"Datacompy_{timestamp}"

        os.mkdir(data_dir)

        report_name_data_dict = {
            os.path.join(data_dir, "Intersection.csv"): comparison.intersect_rows,
            os.path.join(data_dir, "Only In First.csv"): comparison.df1_unq_rows,
            os.path.join(data_dir, "Only In Second.csv"): comparison.df2_unq_rows,
        }

        for name, df in report_name_data_dict.items():

            df.to_csv(name)

        with open(os.path.join(data_dir, "Report.txt"), "w+") as out_file:

            out_file.write(comparison.report())

        return data_dir

    def generate_pandas_profiling_report(self, **kwargs):

        target_csv = kwargs[CSV]

        df = pd.read_csv(target_csv)

        report_title = Path(target_csv).stem

        report = ProfileReport(df, title=report_title)

        timestamp = str(datetime.now().timestamp())

        report_title = f"{report.title}_{timestamp}.html"

        report.to_file(report_title)

        return report_title

    def _get_df_and_name_from_csv(self, csv_file):

        df = pd.read_csv(csv_file)

        name = Path(csv_file).stem

        return df, name

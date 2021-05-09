import kaggle
from pathlib import Path
import pandas as pd


class CovidKaggleDataExplorer:

    def __init__(self):
        self.path = Path(__file__).parent / "data" / "kaggle_covid-19_open_csv_format.csv"
        self.validate_data()
        self.dataframe = self.construct_dataframe()

    def construct_dataframe(self):

        df = pd.read_csv(self.path, encoding='latin-1')
        print("*********")
        print("Dataset has {} rows before clean up. ".format(len(df.index)))
        df = df.dropna(subset=["text_body"])  # drop NaN rows
        print("Dataset has {} rows after clean up. ".format(len(df.index)))
        print("*********")
        df = df.reset_index(drop=True)
        return df

    def validate_data(self):
        if self.path.is_file():
            return

        kaggle.api.authenticate()
        kaggle.api.dataset_download_files('fmitchell259/covid19-medical-paperscsv', path=str(self.path.parent),
                                          unzip=True)

        assert self.path.is_file()

    def get_data(self):
        return [text for text in self.dataframe['text_body']]
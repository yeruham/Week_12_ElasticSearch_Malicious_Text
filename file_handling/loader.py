import pandas as pd


class Loader:

    @staticmethod
    def load_csv_to_df(url):
        df = pd.read_csv(url)
        return df

    @staticmethod
    def load_txt_to_list(path):
        with open(path, 'r') as f:
            weapons = f.read().split('\n')
        return weapons





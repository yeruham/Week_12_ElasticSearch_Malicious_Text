import csv


class Loader:

    @staticmethod
    def load_csv_to_dict(path):
        with open(path, mode='r', newline='', encoding='utf-8') as csvfile:
            data = list(csv.DictReader(csvfile))
        return data


    @staticmethod
    def load_txt_to_list(path):
        with open(path, 'r') as f:
            weapons = f.read().split('\n')
        return weapons